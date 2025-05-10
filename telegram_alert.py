import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Telegram Error: {response.text}")
    else:
        print("📲 Telegram text message sent.")

def send_telegram_photo(image_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {"photo": photo}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
        response = requests.post(url, data=data, files=files)
        if response.status_code != 200:
            print(f"❌ Telegram Photo Error: {response.text}")
        else:
            print("🖼️ Telegram photo sent.")

def wait_for_telegram_reply(timeout=300):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    print("⏳ Waiting for your reply (yes/no)...")
    start_time = time.time()
    last_update_id = None

    while time.time() - start_time < timeout:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            updates = data.get("result", [])
            if updates:
                for update in reversed(updates):
                    update_id = update["update_id"]
                    if last_update_id is None or update_id > last_update_id:
                        last_update_id = update_id
                        message = update.get("message", {}).get("text", "").strip().lower()
                        chat_id = update.get("message", {}).get("chat", {}).get("id")
                        if str(chat_id) == TELEGRAM_CHAT_ID:
                            if message in ["yes", "no"]:
                                print(f"✅ Got reply: {message}")
                                return message
        time.sleep(5)
    print("⌛ Timeout waiting for Telegram reply.")
    return "timeout"
