import datetime
import os
import schedule
import time
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

# Emoji flags for different countries
FLAG_EMOJIS = {
    "USA": "\U0001F1FA\U0001F1F8",
    "CANADA": "\U0001F1E8\U0001F1E6",
    "INDIA": "\U0001F1EE\U0001F1F3",
}

# Only create a single post per run
MAX_POSTS_PER_RUN = 1
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "output"

def parse_birthdays(data: str):
    """Parse GPT birthday text into a list of dicts."""
    records = []
    for line in data.splitlines():
        try:
            name, country, popularity = [part.strip() for part in line.split(",")]
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
    # Ensure we only keep Indian celebrities
    return [r for r in records if r["country"].strip().upper() == "INDIA"]


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


def build_caption(name: str, country: str, zodiac: str) -> str:
    """Create a caption with basic hashtags."""
    flag = FLAG_EMOJIS.get(country.upper(), "")
    hashtags = f"#HappyBirthday #{country.replace(' ', '')}"
    name_tag = f"#{''.join(name.split())}"
    return (
        f"Happy Birthday {name}! {flag} {zodiac}\n"
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
    caption = build_caption(name, country, zodiac)
    prompt_msg = (
        f"Preview ready for {name}.\n{caption}\nPost to Instagram? Reply yes or no."
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

    # Immediate run (for Telegram /run)
    run_bot()

    # Scheduled times
    # Run once per day at 7:30 PM IST (14:00 UTC)
    schedule.every().day.at("14:00").do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(30)
