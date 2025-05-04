from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from database import init_db, add_quotes_from_file, get_random_unused_quote, mark_quote_as_used

def run_bot():
    init_db()
    add_quotes_from_file()

    quote_data = get_random_unused_quote()
    if not quote_data:
        print("❌ No new quotes left to post.")
        return

    quote_id, quote = quote_data
    image_path = create_instagram_post(quote)
    if image_path:
        post_to_instagram(image_path, quote)
        mark_quote_as_used(quote_id)

if __name__ == "__main__":
    run_bot()
