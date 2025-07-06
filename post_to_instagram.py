from instagrapi import Client
import config
import os
import json
from telegram_alert import send_telegram_alert, wait_for_telegram_code, send_error_report


def login_instagram():
    """Login to Instagram handling expired sessions and 2FA via Telegram."""
    cl = Client()
    if os.path.exists("session.json"):
        try:
            cl.load_settings("session.json")
        except Exception as e:
            print(f"⚠️ Failed to load session settings: {e}")

    try:
        cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)
    except Exception as e:
        print(f"🔑 Login requires verification: {e}")
        send_telegram_alert("📲 Instagram verification needed. Please reply with the code.")
        code = wait_for_telegram_code(timeout=600)
        if not code:
            raise Exception("No verification code received")
        cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD, verification_code=code)

    cl.dump_settings("session.json")
    return cl

def post_to_instagram(image_path, caption):
    """Upload the image with the given caption, handling expired sessions."""

    for attempt in range(2):
        try:
            cl = login_instagram()
            cl.photo_upload(path=image_path, caption=caption)
            print("✅ Post uploaded successfully!")
            return
        except Exception as e:
            if (
                ("login_required" in str(e).lower() or "403" in str(e))
                and attempt == 0
            ):
                print("🔄 Session invalid, retrying login...")
                if os.path.exists("session.json"):
                    os.remove("session.json")
                continue
            print("❌ Error uploading post:", e)
            send_error_report("Error uploading post", e)
            break

def save_posted_news(news_title):
    if not os.path.exists("posted_news.json"):
        posted = []
    else:
        with open("posted_news.json", "r") as f:
            posted = json.load(f)
    
    posted.append(news_title)
    with open("posted_news.json", "w") as f:
        json.dump(posted, f)

def is_already_posted(news_title):
    if not os.path.exists("posted_news.json"):
        return False
    with open("posted_news.json", "r") as f:
        posted = json.load(f)
    return news_title in posted
