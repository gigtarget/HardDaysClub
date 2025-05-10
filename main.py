import schedule
import time
from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from quote_generator import generate_and_post_unique_quote
from telegram_alert import send_telegram_photo, wait_for_telegram_reply, send_telegram_alert
from dotenv import load_dotenv

load_dotenv()

def approval_loop(max_hours_wait=3):
    try:
        while True:
            quote = generate_and_post_unique_quote()
            image_path = create_instagram_post(quote)

            hashtags = (
                "\n\n"
                "#onequietpush #quoteoftheday #quietgrit #growthmindset "
                "#dailyquotes #mindsetmatters #innerstrength #softdiscipline "
                "#MotivationMonday #Inspiration #StayMotivated #MotivationalQuotes "
                "#Ambition #Empowerment #MotivationalSpeaker #PositiveVibes "
                "#SelfMotivation #DreamBig"
                "#dailyquotes #mindsetmatters #innerstrength #softdiscipline"
            )
            caption = f"{quote}{hashtags}"

            if image_path:
                send_telegram_photo(image_path, caption)
                reply = wait_for_telegram_reply(timeout=max_hours_wait * 3600)

                if reply == "yes":
                    post_to_instagram(image_path, caption)
                    send_telegram_alert(f"✅ Post approved and uploaded:\n\n{quote}")
                    print("✅ Posted successfully.")
                    break
                elif reply == "no":
                    send_telegram_alert("🔁 You rejected the post. Generating a new one...")
                    print("🔁 Regenerating new image as per user request...")
                    continue
                else:
                    send_telegram_alert("⌛ No reply in 3 hours. Skipping post.")
                    print("⌛ Timeout. Skipping post.")
                    break
    except Exception as e:
        print("❌ Error:", e)
        send_telegram_alert(f"❌ Bot crashed: {e}")

def run_bot():
    approval_loop()

# Schedule times (UTC)
schedule.every().day.at("01:27").do(run_bot)
schedule.every().day.at("14:00").do(run_bot)
schedule.every().day.at("18:00").do(run_bot)

print("🔄 Bot is running. Waiting for scheduled posts...")

while True:
    schedule.run_pending()
    time.sleep(30)
