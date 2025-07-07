import os
import requests
from dotenv import load_dotenv
import subprocess

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

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
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

def handle_command(text):
    if text.strip().lower() == "/run":
        send_message("⚙️ Running the birthday bot now...")
        subprocess.Popen(["python", "birthday_bot.py"])

def run_bot():
    global LAST_UPDATE_ID
    while True:
        updates = get_updates()
        for update in updates.get("result", []):
            LAST_UPDATE_ID = update["update_id"]
            if "message" in update:
                msg_text = update["message"].get("text", "")
                handle_command(msg_text)

if __name__ == "__main__":
    send_message("🤖 Birthday Bot is now listening for commands!")
    run_bot()
