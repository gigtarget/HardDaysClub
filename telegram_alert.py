from pathlib import Path
from dotenv import load_dotenv
import os
import telegram

# Load environment variables
load_dotenv(dotenv_path=Path(".env"))

def send_telegram_alert(message):
    try:
        bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Telegram alert failed: {e}")
