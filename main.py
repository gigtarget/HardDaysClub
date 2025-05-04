from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from quote_generator import generate_and_post_unique_quote
from dotenv import load_dotenv
load_dotenv()  # For local .env support

def run_bot():
    try:
        quote = generate_and_post_unique_quote()
        image_path = create_instagram_post(quote)
        if image_path:
            post_to_instagram(image_path, quote)
    except Exception as e:
        print("❌ Error during execution:", e)

if __name__ == "__main__":
    run_bot()
