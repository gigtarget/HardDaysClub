import csv
import os
from random import choice
from create_post import create_instagram_post
from post_to_instagram import post_to_instagram

def load_quotes():
    with open("quotes.csv", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_used_quotes():
    if not os.path.exists("used_quotes.csv"):
        return set()
    with open("used_quotes.csv", "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_used_quote(quote):
    with open("used_quotes.csv", "a", encoding="utf-8") as f:
        f.write(quote + "\n")

def run_bot():
    all_quotes = load_quotes()
    used_quotes = load_used_quotes()

    new_quotes = [q for q in all_quotes if q not in used_quotes]
    if not new_quotes:
        print("❌ No new quotes left to post.")
        return

    quote = choice(new_quotes)
    image_path = create_instagram_post(quote)
    if image_path:
        post_to_instagram(image_path, quote)
        save_used_quote(quote)

if __name__ == "__main__":
    run_bot()