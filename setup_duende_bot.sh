#!/bin/bash
# Setup duende_bot como servicio permanente
# Corre en background, se reinicia si muere

cd /home/pvrolo/repos/canal
git pull origin main -q
cp duende_bot.py /home/pvrolo/duende_bot.py

# Matar instancia anterior si existe
pkill -f duende_bot.py 2>/dev/null

# Arrancar en background
nohup python3 /home/pvrolo/duende_bot.py >> /home/pvrolo/duende_bot.log 2>&1 &
echo "Duende Bot PID: $!"
