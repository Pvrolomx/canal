"""
DUENDE GIST/LARSON - v2
- Monitorea: Carrie Larson, Mark Gist, Cinthia Valero (solo Gist/Larson)
- Distingue expedientes Cinthia por keywords en asunto/cuerpo
- Recordatorio automatico si Cinthia no responde en 3 dias
- Borradores via Claude API -> Supabase -> Telegram para aprobacion
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
    "banco": "Santander -> Banorte"
}

# Keywords para identificar que un correo de Cinthia es del expediente Gist
GIST_KEYWORDS = ["2110850", "El Dorado", "Gist", "Larson", "dorado"]

# Remitentes directos del expediente (siempre Gist/Larson)
DIRECT_SENDERS = {
    "carrie.larson@gmail.com": "Carrie Larson",
    "gistme@gmail.com": "Mark Gist",
}

# Cinthia — solo si el correo tiene keywords de Gist
CINTHIA_EMAIL = "cvalero@santander.com.mx"
CINTHIA_NAME = "Cinthia Montserrat Valero Cruz"

SYSTEM_PROMPT = """Eres el asistente legal de Rolando "Rolo" Romero Garcia,
abogado expat en Puerto Vallarta (Expat Advisor MX, pvrolomx@yahoo.com.mx).

TU UNICA FUNCION: redactar borradores de respuesta para el expediente Gist/Larson.

EXPEDIENTE — GIST / LARSON / EL DORADO:
- Fideicomiso: 2110850-1
- Condominio: El Dorado, Puerto Vallarta
- Banco actual: Santander (en tramite — contacto: Cinthia Montserrat Valero Cruz, cvalero@santander.com.mx)
- Banco destino: Banorte (SOLO cuando Santander autorice todo)
- Tramite: reconocimiento sustituto beneficiario + sustitucion Santander -> Banorte

PARTES:
- Carrie Larson (carrie.larson@gmail.com, 970-618-5663) — beneficiaria principal
- Mark Elliott Gist (gistme@gmail.com) — co-beneficiario, renuncio como sustituto
  fideicomisario — YA FIRMO carta de renuncia (abril 23, 2026)
- Cinthia Montserrat Valero Cruz (cvalero@santander.com.mx) — Especialista
  Fiduciario Santander, Torre Midtown Guadalajara — interlocutora con el banco

FLUJO DEL TRAMITE (orden estricto):
1. Documentos completos (cartas, IDs, correcciones)
2. Enviar expediente a Santander (Cinthia)
3. Santander revisa y autoriza
4. SOLO cuando Santander aprueba -> contactar Banorte
5. Banorte revisa -> firma notarial final

ESTILO POR DESTINATARIO:
- Carrie / Mark: ingles, conciso, directo, americano
- Cinthia: espanol, profesional, formal pero cordial
- Rolo firma: "Best regards, / Rolo" (en ingles) o "Saludos, / Rolo" (en espanol)

REGLAS:
- NUNCA envies — solo redacta el borrador
- Si te falta informacion: [ROLO: verificar X]
- Si hay adjuntos: [ROLO: revisar adjunto antes de aprobar]

FORMATO DE RESPUESTA:
CONTEXTO: [una linea — quien escribe, sobre que, que propones]
---
[borrador listo para enviar]
[ROLO: notas si aplica]"""

REMINDER_PROMPT = """Eres el asistente legal de Rolo Romero, abogado expat en Puerto Vallarta.

Redacta un recordatorio cordial pero firme en espanol para Cinthia Montserrat Valero Cruz 
(Especialista Fiduciario, Santander Guadalajara) sobre el expediente del Fideicomiso 2110850-1 
(El Dorado, beneficiarios Gist/Larson).

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
    """Determina si un correo de Cinthia pertenece al expediente Gist/Larson"""
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

# ── IMAP ─────────────────────────────────────────────────────────────────────
def fetch_new_emails(tokens):
    emails = []
    try:
        mail = imaplib.IMAP4_SSL(tokens["YAHOO_IMAP_HOST"], int(tokens["YAHOO_IMAP_PORT"]))
        mail.login(tokens["YAHOO_EMAIL"], tokens["YAHOO_APP_PASSWORD"])
        mail.select("INBOX")

        # Correos directos Carrie y Mark
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

        # Correos de Cinthia — solo si son del expediente Gist
        status, data = mail.search(None, "UNSEEN", f'FROM "{CINTHIA_EMAIL}"')
        if status == "OK":
            for msg_id in data[0].split()[-5:]:
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                if status != "OK": continue
                msg = email.message_from_bytes(msg_data[0][1])
                subject = decode_subject(msg.get("Subject", ""))
                body = get_body(msg)
                if not is_gist_email(subject, body):
                    print(f"  Cinthia (ignorado - otro expediente): {subject[:50]}")
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

# ── SUPABASE ─────────────────────────────────────────────────────────────────
def get_supabase(tokens):
    return create_client(tokens["SUPABASE_URL"], tokens["SUPABASE_KEY"])

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
    """Verifica si han pasado 3 dias sin respuesta de Cinthia en expediente Gist"""
    try:
        sb = get_supabase(tokens)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()

        # Buscar el ultimo correo enviado A Cinthia sobre Gist
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

        # Verificar si Cinthia respondio despues de ese envio
        response = sb.table("colmena_email_inbox")\
            .select("id")\
            .eq("expediente", "GIST_LARSON")\
            .eq("sender", CINTHIA_EMAIL)\
            .gt("created_at", last_sent["created_at"])\
            .limit(1)\
            .execute()

        if not response.data:
            print(f"  ALERTA: Sin respuesta de Cinthia desde {last_sent['created_at'][:10]}")
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
def notify_telegram(tokens, sender_name, subject, draft, record_id, is_reminder=False):
    try:
        if is_reminder:
            header = "⏰ *RECORDATORIO — CINTHIA SIN RESPUESTA (3 dias)*\nExpediente: Gist/Larson — Fideicomiso 2110850-1"
        else:
            att = " 📎" if "adjunto" in draft.lower() else ""
            header = f"📬 *DUENDE GIST/LARSON*\nDe: *{sender_name}*{att}\nAsunto: {subject}"

        msg = f"""{header}

{draft[:900]}

---
ID: {record_id} | Aprobar: cambia status a 'aprobado' en Supabase"""

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
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Duende Gist/Larson v2 iniciando...")
    tokens = load_tokens()

    if not tokens.get("YAHOO_APP_PASSWORD"):
        print("ERROR: No se pudieron cargar tokens")
        return

    # 1. Revisar correos nuevos
    print("  Revisando correos nuevos...")
    emails = fetch_new_emails(tokens)
    print(f"  Total correos nuevos del expediente: {len(emails)}")

    for em in emails:
        draft = generate_draft(tokens, em)
        record_id = save_email(tokens, em, draft)
        notify_telegram(tokens, em["sender_name"], em["subject"], draft, record_id)
        time.sleep(2)

    # 2. Verificar recordatorio Cinthia
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
            "body": "Recordatorio automatico generado por el duende",
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

        notify_telegram(tokens, CINTHIA_NAME, "Sin respuesta 3 dias", draft, record_id, is_reminder=True)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Listo.")

if __name__ == "__main__":
    run()
