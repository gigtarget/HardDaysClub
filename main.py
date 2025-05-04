from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from quote_generator import generate_and_post_unique_quote
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env (for local dev)

def run_bot():
    try:
        # Step 1: Get a new unique quote
        quote = generate_and_post_unique_quote()

        # Step 2: Generate Instagram image from quote
        image_path = create_instagram_post(quote)

        # Step 3: Add hashtags to caption
        hashtags = (
            "\n\n"
            "#onequietpush #quoteoftheday #quietgrit #growthmindset "
            "#dailyquotes #mindsetmatters #innerstrength #softdiscipline"
        )
        caption = f"{quote}{hashtags}"

        # Step 4: Post to Instagram
        if image_path:
            post_to_instagram(image_path, caption)

    except Exception as e:
        print("❌ Error during execution:", e)

if __name__ == "__main__":
    run_bot()
