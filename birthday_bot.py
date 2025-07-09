import datetime
import os
import schedule
import time
import json
import re
from telegram_alert import (
    send_telegram_alert,
    send_telegram_photo,
    wait_for_telegram_reply,
)
from openai import OpenAI
from generate_ai_image import generate_ai_image
from post_to_instagram import post_to_instagram

# Setup OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Emoji flags
FLAG_EMOJIS = {
    "USA": "\U0001F1FA\U0001F1F8",
    "CANADA": "\U0001F1E8\U0001F1E6",
    "INDIA": "\U0001F1EE\U0001F1F3",
}

# Only 1 post per run
MAX_POSTS_PER_RUN = 1

# Directories
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "output"

def parse_birthdays(data: str):
    """Parse GPT birthday text into a list of dicts."""
    records = []
    for line in data.splitlines():
        try:
            name, country, popularity = [part.strip() for part in line.split(",")]
            if country.upper() != "INDIA":
                continue  # Skip non-Indian entries
            records.append({
                "name": name,
                "country": country,
                "popularity": int(popularity),
                "date": datetime.datetime.now(datetime.UTC).strftime("%m-%d"),
            })
        except ValueError:
            warn = f"⚠️ Skipped malformed line: {line}"
            print(warn)
            send_telegram_alert(warn)
    return records

def fetch_famous_birthdays_for_today():
    today = datetime.datetime.now(datetime.UTC).strftime("%B %d")
    prompt = (
        f"Give me a list of 5 very famous people born on {today} from India only. "
        "Format each line as: Name,Country,Popularity (0–100) with no numbering or explanations."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        text = response.choices[0].message.content.strip()
        msg = "🧠 Fetched birthday data:\n" + text
        print(msg)
        send_telegram_alert(msg)
        return parse_birthdays(text)
    except Exception as e:
        err = f"❌ OpenAI Error: {e}"
        print(err)
        send_telegram_alert(err)
        return []

def fetch_instagram_handle(name: str) -> str:
    """Search the web for the official Instagram handle of a person."""
    prompt = (
        f"Search the web for the official Instagram username of {name}. "
        "If you cannot find an official account, respond with 'not_found'."
        " Provide the answer strictly in this JSON format:\n"
        "{\n  \"instagram\": \"@username_or_not_found\"\n}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-search-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r"{\s*\"instagram\"\s*:\s*\".*?\"\s*}", content)
        if not match:
            retry_prompt = (
                "Extract and return only the JSON object of the form {\"instagram\": \"@handle\"} "
                f"from the following text:\n{content}"
            )
            retry_response = client.chat.completions.create(
                model="gpt-4o-search-preview",
                messages=[{"role": "user", "content": retry_prompt}]
            )
            retry_content = retry_response.choices[0].message.content.strip()
            match = re.search(r"{\s*\"instagram\"\s*:\s*\".*?\"\s*}", retry_content)
            if not match:
                send_telegram_alert(f"❌ Could not parse Instagram handle for {name}")
                return ""
            json_str = match.group(0)
        else:
            json_str = match.group(0)

        handle = json.loads(json_str).get("instagram", "")
        if handle.lower() in ["not_found", "none", ""]:
            return ""
        return handle
    except Exception as e:
        send_telegram_alert(f"❌ Error fetching Instagram handle for {name}: {e}")
        return ""

# Zodiac sign lookup
ZODIAC_RANGES = [
    ((1, 20), "♑"), ((2, 18), "♒"), ((3, 20), "♓"), ((4, 20), "♈"),
    ((5, 21), "♉"), ((6, 21), "♊"), ((7, 22), "♋"), ((8, 23), "♌"),
    ((9, 23), "♍"), ((10, 23), "♎"), ((11, 22), "♏"), ((12, 21), "♐"),
    ((12, 31), "♑"),
]

def get_zodiac_symbol(month, day):
    for (end_month, end_day), symbol in ZODIAC_RANGES:
        if (month < end_month) or (month == end_month and day <= end_day):
            return symbol
    return ""

def build_caption(name: str, country: str, zodiac: str, instagram_handle: str = "") -> str:
    flag = FLAG_EMOJIS.get(country.upper(), "")
    hashtags = f"#HappyBirthday #{country.replace(' ', '')}"
    name_tag = f"#{''.join(name.split())}"
    handle_line = f"Instagram: {instagram_handle}\n" if instagram_handle else ""
    return (
        f"Happy Birthday {name}! {flag} {zodiac}\n"
        f"{handle_line}"
        f"Celebrating legends from {country}.\n"
        f"{hashtags} {name_tag}"
    )

def create_and_post(person):
    name = person["name"]
    country = person["country"]
    month, day = map(int, person["date"].split("-"))
    zodiac = get_zodiac_symbol(month, day)

    msg = f"🎨 Generating AI image for {name}"
    print(msg)
    send_telegram_alert(msg)

    final_path = generate_ai_image(
        name,
        country,
        zodiac,
        output_path=os.path.join(OUTPUT_DIR, f"{name}_birthday.png"),
    )

    instagram_handle = fetch_instagram_handle(name)
    if instagram_handle:
        send_telegram_alert(f"✅ Found Instagram handle for {name}: {instagram_handle}")
    else:
        send_telegram_alert(f"ℹ️ No official Instagram handle found for {name}")

    caption = build_caption(name, country, zodiac, instagram_handle)
    prompt_msg = (
        f"Preview ready for {name}.\n{caption}\n\nPost to Instagram? Reply yes or no."
    )
    send_telegram_photo(final_path, prompt_msg)

    decision = wait_for_telegram_reply(timeout=10800)
    if decision == "yes":
        msg = f"📤 Posting to Instagram: {caption}"
        print(msg)
        send_telegram_alert(msg)
        post_to_instagram(final_path, caption)
    else:
        send_telegram_alert("🚫 Post cancelled or timed out.")

def run_bot():
    msg = "🔁 Running birthday bot task..."
    print(msg)
    send_telegram_alert(msg)
    try:
        birthdays = fetch_famous_birthdays_for_today()
        if not birthdays:
            msg = "❌ No notable birthdays today."
            print(msg)
            send_telegram_alert(msg)
            return
        birthdays.sort(key=lambda x: int(x.get("popularity", 0)), reverse=True)
        top_people = birthdays[:MAX_POSTS_PER_RUN]
        for person in top_people:
            msg = f"🎉 Creating post for {person['name']} ({person['country']})"
            print(msg)
            send_telegram_alert(msg)
            create_and_post(person)
    except Exception as e:
        err = f"❌ ERROR in birthday bot: {e}"
        print(err)
        send_telegram_alert(err)

if __name__ == "__main__":
    msg = "📅 Birthday bot running..."
    print(msg)
    send_telegram_alert(msg)

    # Immediate run
    run_bot()

    # Run only for India: 7:30 PM IST = 14:00 UTC
    schedule.every().day.at("14:00").do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(30)
