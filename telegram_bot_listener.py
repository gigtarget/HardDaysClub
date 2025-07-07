import os
import time
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
LAST_UPDATE_ID = None

def get_updates():
    global LAST_UPDATE_ID
    url = f"{BASE_URL}/getUpdates"
    if LAST_UPDATE_ID:
        url += f"?offset={LAST_UPDATE_ID + 1}"
    response = requests.get(url)
    return response.json()

def send_message(text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=payload)

def handle_command(command):
    if command.strip().lower() == "/run":
        send_message("✅ Running Birthday Bot...")
        subprocess.Popen(["python3", "birthday_bot.py"])

def run_bot():
    global LAST_UPDATE_ID
    send_message("🤖 Bot Listener Active. Send /run to trigger Birthday Bot.")
    while True:
        updates = get_updates()
        for update in updates.get("result", []):
            LAST_UPDATE_ID = update["update_id"]
            if "message" in update:
                text = update["message"].get("text", "")
                if text:
                    handle_command(text)
        time.sleep(2)

if __name__ == "__main__":
    run_bot()
