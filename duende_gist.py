"""
DUENDE GIST/LARSON - v1
Monitorea correos de Carrie Larson y Mark Gist via IMAP Yahoo
Genera borradores via Claude API
Notifica a Rolo via Telegram
Guarda todo en Supabase

Expediente: Fideicomiso El Dorado C-2 (2110850-1)
Banco: Santander -> Banorte (cuando Santander autorice)
"""
import imaplib, email, json, os, requests, time
from email.header import decode_header
from datetime import datetime, timezone
from supabase import create_client

# ── TOKENS ──────────────────────────────────────────────────────────────────
TOKENS_FILE = os.path.expanduser("~/colmena/keys/TOKENS.md")

def load_tokens():
    t = {}
    try:
        for line in open(TOKENS_FILE):
            line = line.strip()
            for key in ["YAHOO_EMAIL","YAHOO_APP_PASSWORD","YAHOO_IMAP_HOST",
                        "YAHOO_IMAP_PORT","SUPABASE_URL","SUPABASE_KEY",
                        "ANTHROPIC_KEY","BOT_TOKEN","CHAT_ID"]:
                if line.startswith(key + "="):
                    t[key] = line.split("=",1)[1].strip()
    except Exception as e:
        print(f"Error leyendo tokens: {e}")
    return t

# ── CONFIG ───────────────────────────────────────────────────────────────────
MONITORED_SENDERS = [
    "carrie.larson@gmail.com",
    "gistme@gmail.com",
]

SYSTEM_PROMPT = """Eres el asistente legal de Rolando "Rolo" Romero Garcia,
abogado expat en Puerto Vallarta (Expat Advisor MX, pvrolomx@yahoo.com.mx).

TU UNICA FUNCION: redactar borradores de respuesta a correos del expediente Gist/Larson.

EXPEDIENTE — CARRIE LARSON / MARK GIST:
- Asunto: Fideicomiso El Dorado C-2, Fideicomiso 2110850-1
- Condominio: El Dorado, Puerto Vallarta
- Banco actual: Santander (en proceso de tramite)
- Banco destino: Banorte (SOLO cuando Santander haya autorizado todo)
- Tramite: reconocimiento sustituto beneficiario + sustitucion Santander -> Banorte
- Mark Elliott Gist (gistme@gmail.com) — co-beneficiario, renuncio como sustituto
  fideicomisario — YA FIRMO la carta de renuncia (abril 23, 2026)
- Carrie Larson (carrie.larson@gmail.com, 970-618-5663) — beneficiaria principal

FLUJO DEL TRAMITE (en orden estricto):
1. Reunir documentos completos (cartas, IDs, correcciones)
2. Enviar expediente a Santander
3. Santander revisa y autoriza
4. SOLO cuando Santander aprueba -> contactar Banorte
5. Banorte revisa expediente limpio -> firma notarial final

ESTILO: Carrie y Mark son americanos. Responde en ingles, conciso, profesional.
Rolo firma "Saludos, / Rolo" o "Best regards, / Rolo"

REGLAS ABSOLUTAS:
- NUNCA envies nada — solo redacta el borrador
- NUNCA inventes informacion que no tengas
- Si necesitas info que no tienes: [ROLO: verificar X]
- Si hay adjuntos: [ROLO: revisar adjunto antes de aprobar]
- Siempre cierra con: Best regards, / Rolo

FORMATO DE RESPUESTA:
Linea 1: CONTEXTO: [una linea — de quien es, sobre que, que propones]
Linea 2: ---
Resto: el borrador listo para enviar
Ultima linea si aplica: [ROLO: nota para verificar]"""

# ── IMAP ─────────────────────────────────────────────────────────────────────
def fetch_new_emails(tokens):
    """Conecta a Yahoo IMAP y trae correos no vistos de los remitentes monitoreados"""
    emails = []
    try:
        mail = imaplib.IMAP4_SSL(tokens["YAHOO_IMAP_HOST"], int(tokens["YAHOO_IMAP_PORT"]))
        mail.login(tokens["YAHOO_EMAIL"], tokens["YAHOO_APP_PASSWORD"])
        mail.select("INBOX")

        for sender in MONITORED_SENDERS:
            status, data = mail.search(None, "UNSEEN", f'FROM "{sender}"')
            if status != "OK":
                continue
            msg_ids = data[0].split()
            print(f"  {sender}: {len(msg_ids)} correos nuevos")
            for msg_id in msg_ids[-5:]:  # max 5 por sender
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)

                # Decodificar subject
                subject_raw = msg.get("Subject", "")
                subject_parts = decode_header(subject_raw)
                subject = ""
                for part, enc in subject_parts:
                    if isinstance(part, bytes):
                        subject += part.decode(enc or "utf-8", errors="replace")
                    else:
                        subject += str(part)

                # Extraer body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ct = part.get_content_type()
                        if ct == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                            break
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="replace")

                emails.append({
                    "msg_id": msg_id.decode(),
                    "sender": sender,
                    "from": msg.get("From", ""),
                    "subject": subject,
                    "date": msg.get("Date", ""),
                    "body": body[:3000],
                    "has_attachment": any(
                        part.get_filename() for part in msg.walk()
                        if part.get_filename()
                    )
                })

        mail.logout()
    except Exception as e:
        print(f"Error IMAP: {e}")
    return emails

# ── SUPABASE ─────────────────────────────────────────────────────────────────
def save_email_to_supabase(tokens, email_data, draft):
    """Guarda el correo y el borrador en Supabase"""
    try:
        sb = create_client(tokens["SUPABASE_URL"], tokens["SUPABASE_KEY"])
        record = {
            "expediente": "GIST_LARSON",
            "fideicomiso": "2110850-1",
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
        result = sb.table("email_inbox").insert(record).execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        print(f"Error Supabase: {e}")
        return None

# ── CLAUDE API ───────────────────────────────────────────────────────────────
def generate_draft(tokens, email_data):
    """Genera borrador via Claude Sonnet"""
    try:
        has_att = "[ROLO: hay adjunto en este correo, revisa antes de aprobar]\n\n" if email_data["has_attachment"] else ""
        user_content = f"""Correo recibido:
De: {email_data['from']}
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
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_content}]
            },
            timeout=45
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        print(f"Error Claude API: {e}")
        return f"[ERROR generando borrador: {e}]"

# ── TELEGRAM ─────────────────────────────────────────────────────────────────
def notify_telegram(tokens, email_data, draft, record_id):
    """Notifica a Rolo que hay borrador listo"""
    try:
        sender_name = "Carrie Larson" if "carrie" in email_data["sender"] else "Mark Gist"
        att_note = " 📎" if email_data["has_attachment"] else ""
        msg = f"""📬 *DUENDE GIST/LARSON*

De: *{sender_name}*{att_note}
Asunto: {email_data['subject']}

{draft[:800]}

---
ID: {record_id} | Aprobar en Supabase → status: aprobado"""

        requests.post(
            f"https://api.telegram.org/bot{tokens['BOT_TOKEN']}/sendMessage",
            json={
                "chat_id": tokens["CHAT_ID"],
                "text": msg,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        print(f"  Telegram notificado")
    except Exception as e:
        print(f"Error Telegram: {e}")

# ── MAIN ─────────────────────────────────────────────────────────────────────
def run():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Duende Gist/Larson iniciando...")
    tokens = load_tokens()

    if not tokens.get("YAHOO_APP_PASSWORD"):
        print("ERROR: No se pudieron cargar tokens")
        return

    print("  Revisando correos...")
    emails = fetch_new_emails(tokens)
    print(f"  Total correos nuevos: {len(emails)}")

    for em in emails:
        print(f"  Procesando: {em['subject'][:50]}")
        draft = generate_draft(tokens, em)
        record_id = save_email_to_supabase(tokens, em, draft)
        notify_telegram(tokens, em, draft, record_id)
        time.sleep(2)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Listo.")

if __name__ == "__main__":
    run()
