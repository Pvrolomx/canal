"""
DUENDE BOT - v2 (Long Polling - sin webhook ni HTTPS)
Escucha callbacks de botones Telegram via polling
Corre como servicio permanente en el RPi
"""
import os, requests, smtplib, time, json
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
BOT_TOKEN = TOKENS["BOT_TOKEN"]
CHAT_ID = TOKENS["CHAT_ID"]

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
        f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
        json={"callback_query_id": callback_query_id, "text": text},
        timeout=5
    )

def edit_message(chat_id, message_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
        json={"chat_id": chat_id, "message_id": message_id,
              "text": text, "parse_mode": "Markdown"},
        timeout=10
    )

def send_email_smtp(record):
    try:
        # Extraer cuerpo del borrador (despues de ---)
        lines = record["draft"].split("\n")
        body_lines, skip = [], True
        for line in lines:
            if line.strip() == "---":
                skip = False
                continue
            if not skip:
                body_lines.append(line)
        body_text = "\n".join(body_lines).strip()

        to_email = REPLY_TO.get(record["sender"], record["sender"])

        orig = record.get("subject", "")
        if record["sender"] == "SISTEMA_REMINDER":
            subject = "Fideicomiso 2110850-1 El Dorado — Seguimiento"
        elif orig.startswith("Re:"):
            subject = orig
        else:
            subject = f"Re: {orig}"

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
            .eq("id", record["id"]).execute()

        return True, to_email, subject

    except Exception as e:
        return False, str(e), ""

def handle_approve(record_id, cq_id, chat_id, message_id):
    try:
        sb = get_supabase()
        result = sb.table("colmena_email_inbox")\
            .select("*").eq("id", record_id).execute()

        if not result.data:
            answer_callback(cq_id, "Error: registro no encontrado")
            return

        record = result.data[0]

        if record["status"] != "pendiente_aprobacion":
            answer_callback(cq_id, f"Ya procesado: {record['status']}")
            return

        answer_callback(cq_id, "Enviando...")
        ok, to_or_err, subject = send_email_smtp(record)

        if ok:
            edit_message(chat_id, message_id,
                f"✅ *ENVIADO — Gist/Larson*\nPara: {to_or_err}\nAsunto: {subject}\nID: {record_id}")
            print(f"  Enviado: {to_or_err} — {subject[:40]}")
        else:
            answer_callback(cq_id, f"Error al enviar: {to_or_err[:80]}")
            get_supabase().table("colmena_email_inbox")\
                .update({"status": f"error: {str(to_or_err)[:80]}"})\
                .eq("id", record_id).execute()

    except Exception as e:
        answer_callback(cq_id, f"Error: {e}")
        print(f"Error handle_approve: {e}")

def handle_cancel(record_id, cq_id, chat_id, message_id):
    try:
        get_supabase().table("colmena_email_inbox")\
            .update({"status": "cancelado"})\
            .eq("id", record_id).execute()
        answer_callback(cq_id, "Cancelado")
        edit_message(chat_id, message_id, f"🚫 *CANCELADO* — ID: {record_id}")
        print(f"  Cancelado ID: {record_id}")
    except Exception as e:
        answer_callback(cq_id, f"Error: {e}")

def get_updates(offset=None):
    params = {"timeout": 30, "allowed_updates": ["callback_query"]}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
            params=params, timeout=35
        )
        return r.json().get("result", [])
    except:
        return []

def run():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Duende Bot v2 iniciando (polling)...")
    offset = None

    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1

                if "callback_query" not in update:
                    continue

                cq = update["callback_query"]
                data = cq.get("data", "")
                cq_id = cq["id"]
                chat_id = str(cq["message"]["chat"]["id"])
                message_id = cq["message"]["message_id"]

                # Verificar que es Rolo
                if chat_id != str(CHAT_ID):
                    answer_callback(cq_id, "No autorizado")
                    continue

                if ":" not in data:
                    continue

                action, record_id = data.split(":", 1)
                record_id = int(record_id)

                print(f"  Callback: {action} ID:{record_id}")

                if action == "aprobar":
                    handle_approve(record_id, cq_id, chat_id, message_id)
                elif action == "cancelar":
                    handle_cancel(record_id, cq_id, chat_id, message_id)

        except KeyboardInterrupt:
            print("Bot detenido")
            break
        except Exception as e:
            print(f"Error polling: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()
