#!/bin/bash
# cron_wrapper.sh - ejecutado a las 5:45 AM
# 1. Jala ultimo codigo de GitHub
# 2. Corre el briefing de IA
# 3. Verifica que el duende_bot este corriendo

cd /home/pvrolo/repos/canal
git pull origin main -q

# Briefing IA
python3 /home/pvrolo/ai_briefing.py >> /home/pvrolo/ai_briefing.log 2>&1

# Verificar y arrancar duende_bot si no corre
if ! pgrep -f "duende_bot.py" > /dev/null; then
    cp duende_bot.py /home/pvrolo/duende_bot.py
    nohup python3 /home/pvrolo/duende_bot.py >> /home/pvrolo/duende_bot.log 2>&1 &
    echo "[$(date)] Duende Bot arrancado desde cron" >> /home/pvrolo/duende_bot.log
fi
