
import sys
sys.path.insert(0, "/home/pvrolo/repos/fantasma/api")
from alert import get_score, send_email, send_telegram, level_emoji
from datetime import datetime

DASHBOARD = "https://fantasma.duendes.app"

data = get_score()
if not data:
    print("ERROR: no score")
    exit(1)

score = data.get("total_score", 0)
level = data.get("alert_level", "?")
action = data.get("recommended_action", "")
em = level_emoji(score)
today = datetime.utcnow().strftime("%d/%m/%Y")
active = data.get("active_details", [])
active_names = [s.get("signal","?") for s in active]
dr = data.get("dias_rojo", {}).get("summary", {})
red_count = dr.get("currently_red", 0)
red_total = dr.get("total_monitored", 0)

print(f"Score: {score} | Level: {level} | Activas: {active_names}")

tg_lines = [
    f"{em} *FANTASMA* — {today}",
    f"Score: *{score}/100* — {level}",
    f"Accion: {action}",
]
if active_names:
    tg_lines.append("Senales: " + ", ".join(active_names))
tg_lines.append(f"Dias rojo: {red_count}/{red_total}")
tg_lines.append(f"[Ver dashboard]({DASHBOARD})")

r = send_telegram("\n".join(tg_lines))
print("Telegram:", r.get("ok"), r.get("description",""))

email_subj = f"{em} FANTASMA {score}/100 — {level}"
email_body = f"{em} Score: {score}/100 — {level}\n{DASHBOARD}"
r2 = send_email(email_subj, email_body)
print("Email:", r2.get("id", r2.get("error","?")))
