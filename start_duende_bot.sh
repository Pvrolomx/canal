#!/bin/bash
# Arranca duende_bot al iniciar el RPi
sleep 30  # esperar que la red este lista
cd /home/pvrolo/repos/canal
git pull origin main -q
cp duende_bot.py /home/pvrolo/duende_bot.py
nohup python3 /home/pvrolo/duende_bot.py >> /home/pvrolo/duende_bot.log 2>&1 &
echo "[$(date)] Duende Bot arrancado PID:$!" >> /home/pvrolo/duende_bot.log
