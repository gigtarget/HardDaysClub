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
        approved = False
        attempts = 0
        max_attempts = 3

        while not approved and attempts < max_attempts:
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
                reply = wait_for_telegram_reply()

                if reply == "yes":
                    post_to_instagram(image_path, caption)
                    send_telegram_alert(f"✅ New motivational post uploaded:\n\n{quote}")
                    approved = True
                    print("✅ Posted successfully.")
                elif reply == "no":
                    print("🔁 Regenerating a new post on user request...")
                    attempts += 1
                else:
                    print("❌ No valid reply received. Skipping post.")
                    send_telegram_alert("❌ Skipped post due to no valid reply.")
                    break

        if not approved and attempts >= max_attempts:
            print("⚠️ Max attempts reached. No post uploaded.")
            send_telegram_alert("⚠️ Max 'no' replies reached. Skipping today's post.")

    except Exception as e:
        print("❌ Error during post:", e)
        send_telegram_alert(f"❌ Bot failed: {e}")

# Schedule times (UTC)
schedule.every().day.at("01:22").do(run_bot)
schedule.every().day.at("14:00").do(run_bot)
schedule.every().day.at("18:00").do(run_bot)

print("🔄 Bot is running. Waiting for scheduled posts...")

while True:
    schedule.run_pending()
    time.sleep(30)
