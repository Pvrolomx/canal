"""
DUENDE BOT - Telegram webhook handler
Corre como servicio en el RPi en puerto 8443
Recibe callbacks de botones inline y ejecuta acciones
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, requests, smtplib, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from supabase import create_client

TOKENS_FILE = os.path.expanduser("~/colmena/keys/TOKENS.md")

def load_tokens():
    t = {}
    try:
        for line in open(TOKENS_FILE):
            line = line.strip()
            for key in ["YAHOO_EMAIL","YAHOO_APP_PASSWORD","YAHOO_SMTP_HOST",
                        "YAHOO_SMTP_PORT","SUPABASE_URL","SUPABASE_KEY",
                        "BOT_TOKEN","CHAT_ID"]:
                if line.startswith(key + "="):
                    t[key] = line.split("=",1)[1].strip()
    except Exception as e:
        print(f"Error tokens: {e}")
    return t

TOKENS = load_tokens()

REPLY_TO = {
    "carrie.larson@gmail.com": "carrie.larson@gmail.com",
    "gistme@gmail.com": "gistme@gmail.com",
    "cvalero@santander.com.mx": "cvalero@santander.com.mx",
    "SISTEMA_REMINDER": "cvalero@santander.com.mx",
}

def get_supabase():
    return create_client(TOKENS["SUPABASE_URL"], TOKENS["SUPABASE_KEY"])

def answer_callback(callback_query_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKENS['BOT_TOKEN']}/answerCallbackQuery",
        json={"callback_query_id": callback_query_id, "text": text},
        timeout=5
    )

def send_telegram(text, reply_markup=None):
    payload = {
        "chat_id": TOKENS["CHAT_ID"],
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(
        f"https://api.telegram.org/bot{TOKENS['BOT_TOKEN']}/sendMessage",
        json=payload, timeout=10
    )

def edit_telegram_message(chat_id, message_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKENS['BOT_TOKEN']}/editMessageText",
        json={
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "Markdown"
        },
        timeout=10
    )

def send_email_smtp(record):
    """Envia el correo aprobado via SMTP Yahoo"""
    try:
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

        to_email = REPLY_TO.get(record["sender"], record["sender"])

        orig_subject = record.get("subject", "")
        if record["sender"] == "SISTEMA_REMINDER":
            subject = "Fideicomiso 2110850-1 El Dorado — Seguimiento"
        elif orig_subject.startswith("Re:"):
            subject = orig_subject
        else:
            subject = f"Re: {orig_subject}"

        msg = MIMEMultipart()
        msg["From"] = TOKENS["YAHOO_EMAIL"]
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain", "utf-8"))

        smtp = smtplib.SMTP_SSL(
            TOKENS.get("YAHOO_SMTP_HOST", "smtp.mail.yahoo.com"),
            int(TOKENS.get("YAHOO_SMTP_PORT", 465))
        )
        smtp.login(TOKENS["YAHOO_EMAIL"], TOKENS["YAHOO_APP_PASSWORD"])
        smtp.sendmail(TOKENS["YAHOO_EMAIL"], to_email, msg.as_string())
        smtp.quit()

        # Registrar ROLO_SENT
        sb = get_supabase()
        sb.table("colmena_email_inbox").insert({
            "expediente": record["expediente"],
            "fideicomiso": record.get("fideicomiso", ""),
            "sender": "ROLO_SENT",
            "from_header": TOKENS["YAHOO_EMAIL"],
            "subject": subject,
            "date_received": datetime.now(timezone.utc).isoformat(),
            "body": body_text,
            "has_attachment": False,
            "draft": "",
            "status": "enviado",
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()

        # Marcar original como enviado
        sb.table("colmena_email_inbox")\
            .update({"status": "enviado"})\
            .eq("id", record["id"])\
            .execute()

        return True, to_email, subject

    except Exception as e:
        return False, str(e), ""

def handle_approve(record_id, callback_query_id, chat_id, message_id):
    """Procesa aprobacion de borrador"""
    try:
        sb = get_supabase()
        result = sb.table("colmena_email_inbox")\
            .select("*").eq("id", record_id).execute()

        if not result.data:
            answer_callback(callback_query_id, "❌ Registro no encontrado")
            return

        record = result.data[0]

        if record["status"] != "pendiente_aprobacion":
            answer_callback(callback_query_id, f"⚠️ Ya procesado: {record['status']}")
            return

        answer_callback(callback_query_id, "⏳ Enviando...")

        ok, to_or_err, subject = send_email_smtp(record)

        if ok:
            edit_telegram_message(
                chat_id, message_id,
                f"✅ *ENVIADO — Gist/Larson*\nPara: {to_or_err}\nAsunto: {subject}\nID: {record_id}"
            )
        else:
            answer_callback(callback_query_id, f"❌ Error: {to_or_err}")
            sb.table("colmena_email_inbox")\
                .update({"status": f"error: {str(to_or_err)[:80]}"})\
                .eq("id", record_id).execute()

    except Exception as e:
        answer_callback(callback_query_id, f"❌ Error: {e}")

def handle_cancel(record_id, callback_query_id, chat_id, message_id):
    """Cancela el borrador"""
    try:
        sb = get_supabase()
        sb.table("colmena_email_inbox")\
            .update({"status": "cancelado"})\
            .eq("id", record_id).execute()
        answer_callback(callback_query_id, "🚫 Cancelado")
        edit_telegram_message(chat_id, message_id, f"🚫 *CANCELADO* — ID: {record_id}")
    except Exception as e:
        answer_callback(callback_query_id, f"❌ Error: {e}")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

        # Procesar en thread para no bloquear
        threading.Thread(target=self.process_update, args=(body,)).start()

    def process_update(self, body):
        try:
            if "callback_query" not in body:
                return

            cq = body["callback_query"]
            data = cq.get("data", "")
            cq_id = cq["id"]
            chat_id = cq["message"]["chat"]["id"]
            message_id = cq["message"]["message_id"]

            # Verificar que es Rolo
            if str(chat_id) != str(TOKENS.get("CHAT_ID", "")):
                answer_callback(cq_id, "⛔ No autorizado")
                return

            # Parsear accion y record_id
            # Formato: "aprobar:123" o "cancelar:123"
            if ":" not in data:
                return

            action, record_id = data.split(":", 1)
            record_id = int(record_id)

            if action == "aprobar":
                handle_approve(record_id, cq_id, chat_id, message_id)
            elif action == "cancelar":
                handle_cancel(record_id, cq_id, chat_id, message_id)

        except Exception as e:
            print(f"Error procesando update: {e}")

    def log_message(self, format, *args):
        pass  # Silenciar logs HTTP

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Duende Bot iniciando en puerto 8444...")
    server = HTTPServer(("0.0.0.0", 8444), WebhookHandler)
    print("Listo — escuchando callbacks de Telegram")
    server.serve_forever()
