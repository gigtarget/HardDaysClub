import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Track the last processed Telegram update so we don't reprocess old messages
_LAST_UPDATE_ID = None

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

def wait_for_telegram_reply(timeout=10800):  # 3 hours
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    print("⏳ Waiting for your reply (yes/no)...")
    start_time = time.time()
    last_update_id = None

    # Skip old messages
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        updates = data.get("result", [])
        if updates:
            last_update_id = updates[-1]["update_id"]

    while time.time() - start_time < timeout:
        response = requests.get(url, params={"offset": (last_update_id + 1) if last_update_id else None})
        if response.status_code == 200:
            data = response.json()
            updates = data.get("result", [])
            for update in updates:
                last_update_id = update["update_id"]
                message = update.get("message", {}).get("text", "").strip().lower()
                chat_id = update.get("message", {}).get("chat", {}).get("id")
                if str(chat_id) == TELEGRAM_CHAT_ID and message in ["yes", "no"]:
                    print(f"✅ Got reply: {message}")
                    return message
        time.sleep(5)

    print("⌛ Timeout waiting for Telegram reply.")
    return "timeout"

def wait_for_telegram_code(timeout=300):
    """Wait for any text reply on Telegram and return it.

    Parameters
    ----------
    timeout : int
        Seconds to wait before giving up.

    Returns
    -------
    str or None
        The message text or ``None`` if timed out.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    print("⏳ Waiting for your verification code...")
    start_time = time.time()
    last_update_id = None

    # Skip old messages
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        updates = data.get("result", [])
        if updates:
            last_update_id = updates[-1]["update_id"]

    while time.time() - start_time < timeout:
        response = requests.get(url, params={"offset": (last_update_id + 1) if last_update_id else None})
        if response.status_code == 200:
            data = response.json()
            updates = data.get("result", [])
            for update in updates:
                last_update_id = update["update_id"]
                message = update.get("message", {}).get("text", "").strip()
                chat_id = update.get("message", {}).get("chat", {}).get("id")
                if str(chat_id) == TELEGRAM_CHAT_ID and message:
                    print(f"✅ Got code: {message}")
                    return message
        time.sleep(5)

    print("⌛ Timeout waiting for Telegram code.")
    return None

def init_telegram_updates():
    """Initialize the last update ID to ignore old messages."""
    global _LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        updates = data.get("result", [])
        if updates:
            _LAST_UPDATE_ID = updates[-1]["update_id"]

def check_for_command(command="/run"):
    """Return True if the specified command was sent via Telegram."""
    global _LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"offset": (_LAST_UPDATE_ID + 1) if _LAST_UPDATE_ID else None}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        updates = data.get("result", [])
        for update in updates:
            _LAST_UPDATE_ID = update["update_id"]
            message = update.get("message", {}).get("text", "").strip().lower()
            chat_id = update.get("message", {}).get("chat", {}).get("id")
            valid = [command.lower(), command.lstrip("/").lower()]
            if str(chat_id) == TELEGRAM_CHAT_ID and message in valid:
                return True
    return False
