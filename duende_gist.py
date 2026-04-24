"""
DUENDE GIST/LARSON - v3
- Monitorea IMAP: Carrie, Mark, Cinthia (solo Gist keywords)
- Genera borradores via Claude -> Supabase -> Telegram
- Envia correos aprobados via SMTP y registra ROLO_SENT
- Recordatorio automatico 3 dias sin respuesta Cinthia
"""
import imaplib, email, json, os, requests, time, smtplib
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
from supabase import create_client

# ── TOKENS ───────────────────────────────────────────────────────────────────
TOKENS_FILE = os.path.expanduser("~/colmena/keys/TOKENS.md")

def load_tokens():
    t = {}
    try:
        for line in open(TOKENS_FILE):
            line = line.strip()
            for key in ["YAHOO_EMAIL","YAHOO_APP_PASSWORD","YAHOO_IMAP_HOST",
                        "YAHOO_IMAP_PORT","YAHOO_SMTP_HOST","YAHOO_SMTP_PORT",
                        "SUPABASE_URL","SUPABASE_KEY","ANTHROPIC_KEY",
                        "BOT_TOKEN","CHAT_ID"]:
                if line.startswith(key + "="):
                    t[key] = line.split("=",1)[1].strip()
    except Exception as e:
        print(f"Error leyendo tokens: {e}")
    return t

# ── CONFIG ────────────────────────────────────────────────────────────────────
EXPEDIENTE_GIST = {
    "nombre": "GIST_LARSON",
    "fideicomiso": "2110850-1",
    "condominio": "El Dorado",
}

GIST_KEYWORDS = ["2110850", "El Dorado", "Gist", "Larson", "dorado"]

DIRECT_SENDERS = {
    "carrie.larson@gmail.com": "Carrie Larson",
    "gistme@gmail.com": "Mark Gist",
}

CINTHIA_EMAIL = "cvalero@santander.com.mx"
CINTHIA_NAME = "Cinthia Montserrat Valero Cruz"

# Destinatarios para envios salientes por expediente
REPLY_TO = {
    "carrie.larson@gmail.com": "carrie.larson@gmail.com",
    "gistme@gmail.com": "gistme@gmail.com",
    "cvalero@santander.com.mx": "cvalero@santander.com.mx",
    "SISTEMA_REMINDER": "cvalero@santander.com.mx",
}

SYSTEM_PROMPT = """Eres el asistente legal de Rolando "Rolo" Romero Garcia,
abogado expat en Puerto Vallarta (Expat Advisor MX, pvrolomx@yahoo.com.mx).

TU UNICA FUNCION: redactar borradores de respuesta para el expediente Gist/Larson.

EXPEDIENTE — GIST / LARSON / EL DORADO:
- Fideicomiso: 2110850-1
- Condominio: El Dorado, Puerto Vallarta
- Banco actual: Santander (contacto: Cinthia Montserrat Valero Cruz, cvalero@santander.com.mx)
- Banco destino: Banorte (SOLO cuando Santander autorice todo)
- Tramite: reconocimiento sustituto beneficiario + sustitucion Santander -> Banorte

PARTES:
- Carrie Larson (carrie.larson@gmail.com, 970-618-5663) — beneficiaria principal
- Mark Elliott Gist (gistme@gmail.com) — co-beneficiario, renuncio como sustituto
  fideicomisario — YA FIRMO carta de renuncia (abril 23, 2026)
- Cinthia Montserrat Valero Cruz (cvalero@santander.com.mx) — Especialista
  Fiduciario Santander, Torre Midtown Guadalajara

FLUJO DEL TRAMITE (orden estricto):
1. Documentos completos (cartas, IDs, correcciones)
2. Enviar expediente a Santander (Cinthia)
3. Santander revisa y autoriza
4. SOLO cuando Santander aprueba -> contactar Banorte
5. Banorte revisa -> firma notarial final

ESTILO POR DESTINATARIO:
- Carrie / Mark: ingles, conciso, directo
- Cinthia: espanol, profesional, cordial
- Firma: "Best regards, / Rolo" (ingles) o "Saludos, / Rolo" (espanol)

REGLAS:
- NUNCA envies — solo redacta el borrador
- Si te falta informacion: [ROLO: verificar X]
- Si hay adjuntos: [ROLO: revisar adjunto antes de aprobar]

FORMATO:
CONTEXTO: [una linea — quien escribe, sobre que, que propones]
---
[borrador listo para enviar]
[ROLO: notas si aplica]"""

REMINDER_PROMPT = """Eres el asistente legal de Rolo Romero, abogado expat en Puerto Vallarta.

Redacta un recordatorio cordial pero firme en espanol para Cinthia Montserrat Valero Cruz
(Especialista Fiduciario, Santander Guadalajara) sobre el Fideicomiso 2110850-1 (El Dorado, Gist/Larson).

Han pasado 3 dias sin respuesta. El recordatorio debe:
- Ser breve (maximo 5 lineas)
- Mencionar el numero de fideicomiso
- Preguntar el estatus del tramite
- Ser cordial, no agresivo
- Firmar: Saludos, / Rolo / Expat Advisor MX

FORMATO:
CONTEXTO: Recordatorio 3 dias sin respuesta de Cinthia — Fideicomiso 2110850-1
---
[borrador del recordatorio]"""

# ── HELPERS ──────────────────────────────────────────────────────────────────
def is_gist_email(subject, body):
    text = (subject + " " + body).lower()
    return any(kw.lower() in text for kw in GIST_KEYWORDS)

def decode_subject(raw):
    parts = decode_header(raw or "")
    result = ""
    for part, enc in parts:
        if isinstance(part, bytes):
            result += part.decode(enc or "utf-8", errors="replace")
        else:
            result += str(part)
    return result

def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
        except:
            pass
    return body[:3000]

def get_supabase(tokens):
    return create_client(tokens["SUPABASE_URL"], tokens["SUPABASE_KEY"])

# ── IMAP ─────────────────────────────────────────────────────────────────────
def fetch_new_emails(tokens):
    emails = []
    try:
        mail = imaplib.IMAP4_SSL(tokens["YAHOO_IMAP_HOST"], int(tokens["YAHOO_IMAP_PORT"]))
        mail.login(tokens["YAHOO_EMAIL"], tokens["YAHOO_APP_PASSWORD"])
        mail.select("INBOX")

        for sender_email, sender_name in DIRECT_SENDERS.items():
            status, data = mail.search(None, "UNSEEN", f'FROM "{sender_email}"')
            if status != "OK": continue
            for msg_id in data[0].split()[-5:]:
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                if status != "OK": continue
                msg = email.message_from_bytes(msg_data[0][1])
                subject = decode_subject(msg.get("Subject", ""))
                body = get_body(msg)
                has_att = any(p.get_filename() for p in msg.walk() if p.get_filename())
                emails.append({
                    "msg_id": msg_id.decode(),
                    "sender": sender_email,
                    "sender_name": sender_name,
                    "from": msg.get("From", ""),
                    "subject": subject,
                    "date": msg.get("Date", ""),
                    "body": body,
                    "has_attachment": has_att,
                    "expediente": "GIST_LARSON"
                })
                print(f"  Nuevo de {sender_name}: {subject[:50]}")

        status, data = mail.search(None, "UNSEEN", f'FROM "{CINTHIA_EMAIL}"')
        if status == "OK":
            for msg_id in data[0].split()[-5:]:
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                if status != "OK": continue
                msg = email.message_from_bytes(msg_data[0][1])
                subject = decode_subject(msg.get("Subject", ""))
                body = get_body(msg)
                if not is_gist_email(subject, body):
                    print(f"  Cinthia ignorado (otro expediente): {subject[:40]}")
                    continue
                has_att = any(p.get_filename() for p in msg.walk() if p.get_filename())
                emails.append({
                    "msg_id": msg_id.decode(),
                    "sender": CINTHIA_EMAIL,
                    "sender_name": CINTHIA_NAME,
                    "from": msg.get("From", ""),
                    "subject": subject,
                    "date": msg.get("Date", ""),
                    "body": body,
                    "has_attachment": has_att,
                    "expediente": "GIST_LARSON"
                })
                print(f"  Nuevo de Cinthia (Gist): {subject[:50]}")

        mail.logout()
    except Exception as e:
        print(f"Error IMAP: {e}")
    return emails

# ── SMTP — ENVIO APROBADO ─────────────────────────────────────────────────────
def send_approved_emails(tokens):
    """Busca borradores aprobados en Supabase y los envia via SMTP"""
    try:
        sb = get_supabase(tokens)
        result = sb.table("colmena_email_inbox")\
            .select("*")\
            .eq("status", "aprobado")\
            .eq("expediente", "GIST_LARSON")\
            .execute()

        if not result.data:
            return

        print(f"  Correos aprobados para enviar: {len(result.data)}")

        smtp = smtplib.SMTP_SSL(
            tokens.get("YAHOO_SMTP_HOST", "smtp.mail.yahoo.com"),
            int(tokens.get("YAHOO_SMTP_PORT", 465))
        )
        smtp.login(tokens["YAHOO_EMAIL"], tokens["YAHOO_APP_PASSWORD"])

        for record in result.data:
            try:
                # Extraer borrador — quitar la linea CONTEXTO
                draft_lines = record["draft"].split("\n")
                body_lines = []
                skip = True
                for line in draft_lines:
                    if line.strip() == "---":
                        skip = False
                        continue
                    if not skip:
                        body_lines.append(line)
                body_text = "\n".join(body_lines).strip()

                # Destinatario
                to_email = REPLY_TO.get(record["sender"], record["sender"])

                # Asunto — Re: si es respuesta, subject original si es reminder
                if record["sender"] == "SISTEMA_REMINDER":
                    subject = f"Fideicomiso 2110850-1 El Dorado — Seguimiento"
                else:
                    orig_subject = record.get("subject", "")
                    subject = orig_subject if orig_subject.startswith("Re:") else f"Re: {orig_subject}"

                # Armar mensaje
                msg = MIMEMultipart()
                msg["From"] = tokens["YAHOO_EMAIL"]
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body_text, "plain", "utf-8"))

                smtp.sendmail(tokens["YAHOO_EMAIL"], to_email, msg.as_string())
                print(f"  Enviado a {to_email}: {subject[:50]}")

                # Registrar como ROLO_SENT en Supabase
                sent_record = {
                    "expediente": "GIST_LARSON",
                    "fideicomiso": EXPEDIENTE_GIST["fideicomiso"],
                    "sender": "ROLO_SENT",
                    "from_header": tokens["YAHOO_EMAIL"],
                    "subject": subject,
                    "date_received": datetime.now(timezone.utc).isoformat(),
                    "body": body_text,
                    "has_attachment": False,
                    "draft": "",
                    "status": "enviado",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                sb.table("colmena_email_inbox").insert(sent_record).execute()

                # Marcar original como enviado
                sb.table("colmena_email_inbox")\
                    .update({"status": "enviado"})\
                    .eq("id", record["id"])\
                    .execute()

                # Notificar Telegram
                notify_telegram(
                    tokens,
                    f"Enviado a {to_email}",
                    subject,
                    f"CONTEXTO: Correo enviado exitosamente\n---\n{body_text[:300]}",
                    record["id"],
                    is_sent=True
                )
                time.sleep(1)

            except Exception as e:
                print(f"  Error enviando correo ID {record['id']}: {e}")
                sb.table("colmena_email_inbox")\
                    .update({"status": f"error_envio: {str(e)[:100]}"})\
                    .eq("id", record["id"])\
                    .execute()

        smtp.quit()

    except Exception as e:
        print(f"Error SMTP: {e}")

# ── SUPABASE ─────────────────────────────────────────────────────────────────
def save_email(tokens, email_data, draft):
    try:
        sb = get_supabase(tokens)
        record = {
            "expediente": email_data["expediente"],
            "fideicomiso": EXPEDIENTE_GIST["fideicomiso"],
            "sender": email_data["sender"],
            "from_header": email_data["from"],
            "subject": email_data["subject"],
            "date_received": email_data["date"],
            "body": email_data["body"],
            "has_attachment": email_data["has_attachment"],
            "draft": draft,
            "status": "pendiente_aprobacion",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        result = sb.table("colmena_email_inbox").insert(record).execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        print(f"Error Supabase save: {e}")
        return None

def check_cinthia_reminder(tokens):
    try:
        sb = get_supabase(tokens)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()

        sent = sb.table("colmena_email_inbox")\
            .select("*")\
            .eq("expediente", "GIST_LARSON")\
            .eq("sender", "ROLO_SENT")\
            .eq("status", "enviado")\
            .lt("created_at", cutoff)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()

        if not sent.data:
            return False

        last_sent = sent.data[0]

        response = sb.table("colmena_email_inbox")\
            .select("id")\
            .eq("expediente", "GIST_LARSON")\
            .eq("sender", CINTHIA_EMAIL)\
            .gt("created_at", last_sent["created_at"])\
            .limit(1)\
            .execute()

        if not response.data:
            print(f"  ALERTA: Sin respuesta Cinthia desde {last_sent['created_at'][:10]}")
            return True
        return False
    except Exception as e:
        print(f"Error check reminder: {e}")
        return False

# ── CLAUDE API ────────────────────────────────────────────────────────────────
def generate_draft(tokens, email_data=None, is_reminder=False):
    try:
        system = REMINDER_PROMPT if is_reminder else SYSTEM_PROMPT
        if is_reminder:
            user_content = "Genera el recordatorio para Cinthia — 3 dias sin respuesta."
        else:
            has_att = "[ROLO: hay adjunto, revisa antes de aprobar]\n\n" if email_data["has_attachment"] else ""
            user_content = f"""Correo recibido:
De: {email_data['sender_name']} <{email_data['sender']}>
Asunto: {email_data['subject']}
Fecha: {email_data['date']}
{has_att}
Contenido:
{email_data['body']}

Genera el borrador de respuesta para Rolo."""

        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": tokens["ANTHROPIC_KEY"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 800,
                "system": system,
                "messages": [{"role": "user", "content": user_content}]
            },
            timeout=45
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        print(f"Error Claude API: {e}")
        return f"[ERROR generando borrador: {e}]"

# ── TELEGRAM ──────────────────────────────────────────────────────────────────
def notify_telegram(tokens, sender_name, subject, draft, record_id,
                    is_reminder=False, is_sent=False):
    try:
        if is_sent:
            header = f"✅ *ENVIADO — Gist/Larson*\nPara: {sender_name}"
        elif is_reminder:
            header = "⏰ *RECORDATORIO — CINTHIA 3 DIAS SIN RESPUESTA*\nFideicomiso 2110850-1"
        else:
            att = " 📎" if "adjunto" in draft.lower() else ""
            header = f"📬 *DUENDE GIST/LARSON*\nDe: *{sender_name}*{att}\nAsunto: {subject}"

        msg = f"""{header}

{draft[:900]}

---
ID Supabase: {record_id}"""

        if not is_sent:
            msg += "\nPara aprobar: cambia status a *aprobado* en tabla colmena_email_inbox"

        requests.post(
            f"https://api.telegram.org/bot{tokens['BOT_TOKEN']}/sendMessage",
            json={"chat_id": tokens["CHAT_ID"], "text": msg, "parse_mode": "Markdown"},
            timeout=10
        )
        print(f"  Telegram OK")
    except Exception as e:
        print(f"Error Telegram: {e}")

# ── MAIN ──────────────────────────────────────────────────────────────────────
def run():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Duende Gist/Larson v3 iniciando...")
    tokens = load_tokens()

    if not tokens.get("YAHOO_APP_PASSWORD"):
        print("ERROR: No se pudieron cargar tokens")
        return

    # 1. Enviar correos aprobados
    print("  Revisando aprobados para enviar...")
    send_approved_emails(tokens)

    # 2. Revisar correos nuevos
    print("  Revisando correos nuevos...")
    emails = fetch_new_emails(tokens)
    print(f"  Total nuevos del expediente: {len(emails)}")

    for em in emails:
        draft = generate_draft(tokens, em)
        record_id = save_email(tokens, em, draft)
        notify_telegram(tokens, em["sender_name"], em["subject"], draft, record_id)
        time.sleep(2)

    # 3. Verificar recordatorio Cinthia
    print("  Verificando recordatorio Cinthia...")
    if check_cinthia_reminder(tokens):
        draft = generate_draft(tokens, is_reminder=True)
        record = {
            "expediente": "GIST_LARSON",
            "fideicomiso": EXPEDIENTE_GIST["fideicomiso"],
            "sender": "SISTEMA_REMINDER",
            "from_header": "Duende Gist/Larson",
            "subject": "RECORDATORIO: Sin respuesta Cinthia 3 dias",
            "date_received": datetime.now(timezone.utc).isoformat(),
            "body": "Recordatorio automatico",
            "has_attachment": False,
            "draft": draft,
            "status": "pendiente_aprobacion",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        try:
            sb = get_supabase(tokens)
            result = sb.table("colmena_email_inbox").insert(record).execute()
            record_id = result.data[0]["id"] if result.data else None
        except Exception as e:
            print(f"Error guardando reminder: {e}")
            record_id = None
        notify_telegram(tokens, CINTHIA_NAME, "Sin respuesta 3 dias",
                       draft, record_id, is_reminder=True)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Listo.")

if __name__ == "__main__":
    run()
