#!/bin/bash

echo "🚀 Telegram History Sync (Local execution) starting..."
echo "To stop, press Ctrl+C"

# 가상환경이 있다면 활성화 (예: source venv/bin/activate)
# pip install telethon python-dotenv

while true; do
    echo "--------------------------------------------------"
    echo "Running sync_history.py at $(date)"
    python3 sync_history.py
    
    echo "Batch finished or crashed. Resting for 10 seconds before restart..."
    sleep 10
done
