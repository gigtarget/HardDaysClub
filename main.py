import schedule
import time
from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from quote_generator import generate_and_post_unique_quote
from dotenv import load_dotenv

load_dotenv()

def run_bot():
    try:
        quote = generate_and_post_unique_quote()
        image_path = create_instagram_post(quote)

        hashtags = (
            "\n\n"
            "#onequietpush #quoteoftheday #quietgrit #growthmindset "
            "#dailyquotes #mindsetmatters #innerstrength #softdiscipline"
        )
        caption = f"{quote}{hashtags}"

        if image_path:
            post_to_instagram(image_path, caption)
        print("✅ Posted successfully.")
    except Exception as e:
        print("❌ Error during post:", e)

# Schedule times (UTC)
schedule.every().day.at("09:00").do(run_bot)
schedule.every().day.at("14:00").do(run_bot)
schedule.every().day.at("19:00").do(run_bot)

print("🔄 Bot is running. Waiting for scheduled posts...")

while True:
    schedule.run_pending()
    time.sleep(30)
