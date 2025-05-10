
import schedule
import time
from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from quote_generator import generate_and_post_unique_quote
from telegram_alert import send_telegram_photo, wait_for_telegram_reply, send_telegram_alert
from dotenv import load_dotenv

load_dotenv()

def run_bot():
    try:
        # Step 1: Generate content
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

        # Step 2: Send image to Telegram
        send_telegram_photo(image_path, caption)

        while True:
            # Step 3: Wait for reply for up to 3 hours (10800 seconds)
            reply = wait_for_telegram_reply(timeout=10800)

            if reply == "yes":
                post_to_instagram(image_path, caption)
                send_telegram_alert(f"✅ Post approved and uploaded:\n\n{quote}")
                print("✅ Posted successfully.")
                break
            elif reply == "no":
                # If "no", generate one new image and repeat this wait loop
                quote = generate_and_post_unique_quote()
                image_path = create_instagram_post(quote)
                caption = f"{quote}{hashtags}"
                send_telegram_photo(image_path, caption)
            elif reply == "timeout":
                send_telegram_alert("⌛ No reply in 3 hours. Skipping post.")
                print("⌛ Timeout. Skipping post.")
                break
            else:
                # Ignore unrelated replies
                continue

    except Exception as e:
        print("❌ Error during post:", e)
        send_telegram_alert(f"❌ Bot crashed: {e}")

# Schedule times (UTC)
schedule.every().day.at("01:31").do(run_bot)
schedule.every().day.at("14:00").do(run_bot)
schedule.every().day.at("18:00").do(run_bot)

print("🔄 Bot is running. Waiting for scheduled posts...")

while True:
    schedule.run_pending()
    time.sleep(30)
