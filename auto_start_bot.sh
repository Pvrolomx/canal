#!/bin/bash
# auto_start_bot.sh
# Este script se ejecuta una vez para arrancar el duende_bot
# El cron lo llama y el bot queda corriendo en background

BOT_LOG="/home/pvrolo/duende_bot.log"
BOT_SCRIPT="/home/pvrolo/duende_bot.py"

# Verificar si ya esta corriendo
if pgrep -f "duende_bot.py" > /dev/null; then
    echo "[$(date)] Duende Bot ya corre" >> $BOT_LOG
    exit 0
fi

# Jalar ultimo codigo
cd /home/pvrolo/repos/canal
git pull origin main -q
cp duende_bot.py $BOT_SCRIPT

# Arrancar
nohup python3 $BOT_SCRIPT >> $BOT_LOG 2>&1 &
echo "[$(date)] Duende Bot arrancado PID:$!" >> $BOT_LOG
