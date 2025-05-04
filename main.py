import asyncio
from fetch_news import fetch_top_news
from generate_ai_image import generate_ai_image
from create_post import create_instagram_post
from post_to_instagram import post_to_instagram, save_posted_news, is_already_posted
from summarize_news import generate_headline_and_caption

def run_bot():
    news_title, news_summary = fetch_top_news()
    
    if not news_title:
        print("❌ No news found.")
        return
    
    if is_already_posted(news_title):
        print("❌ News already posted. Skipping.")
        return

    headline, caption = generate_headline_and_caption(news_summary)

    image_path = generate_ai_image(headline)
    if image_path:
        final_post_path = create_instagram_post(image_path, headline)
        if final_post_path:
            post_to_instagram(final_post_path, caption)
            save_posted_news(news_title)

if __name__ == "__main__":
    run_bot()
