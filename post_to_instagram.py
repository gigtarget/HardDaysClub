from instagrapi import Client
import config
import os
import json

def post_to_instagram(image_path, caption):
    try:
        cl = Client()
        cl.load_settings("session.json")
        cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)

        cl.photo_upload(
            path=image_path,
            caption=caption
        )

        print("✅ Post uploaded successfully!")

    except Exception as e:
        print("❌ Error uploading post:", e)

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
