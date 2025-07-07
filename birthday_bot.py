import datetime
import os
import schedule
import time
from PIL import Image, ImageDraw, ImageFont
from telegram_alert import send_telegram_alert, send_telegram_photo
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
    return records


def fetch_famous_birthdays_for_today():
    today = datetime.datetime.now(datetime.UTC).strftime("%B %d")
    prompt = (
        f"Give me a list of 5 very famous people born on {today}. "
        "Only include people from USA, Canada, or India. "
        "Format: Name,Country,Popularity (0–100), no numbering, no explanations."
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

def compose_birthday_image(name, country, zodiac, base_image, output_path):
    print(f"🖼️ Composing image for {name}")
    image = Image.open(base_image).convert("RGBA")
    draw = ImageDraw.Draw(image)

    font_path = os.path.join(TEMPLATES_DIR, "OpenSans-Bold.ttf")
    font = ImageFont.truetype(font_path, 80)

    text = f"HAPPY BIRTHDAY {name.upper()}"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (image.width - text_w) // 2
    y = image.height - text_h - 40
    draw.text((x, y), text, font=font, fill="white")

    draw.text((40, 40), zodiac, font=font, fill="white")
    flag = FLAG_EMOJIS.get(country.upper(), country.upper())
    draw.text((image.width - 200, 40), flag, font=font, fill="white")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.convert("RGB").save(output_path)
    send_telegram_alert(f"🖼️ Image composed for {name}")
    return output_path

def create_and_post(person):
    name = person["name"]
    country = person["country"]
    month, day = map(int, person["date"].split("-"))
    zodiac = get_zodiac_symbol(month, day)

    msg = f"🎨 Generating AI image for {name}"
    print(msg)
    send_telegram_alert(msg)
    ai_path = generate_ai_image(
        name,
        output_path=os.path.join(OUTPUT_DIR, f"{name}_ai.png"),
    )
    final_path = compose_birthday_image(
        name,
        country,
        zodiac,
        ai_path,
        os.path.join(OUTPUT_DIR, f"{name}_birthday.png"),
    )
    caption = f"Honoring {name}! Born on this day."
    msg = f"📤 Posting to Instagram: {caption}"
    print(msg)
    send_telegram_alert(msg)
    send_telegram_photo(final_path, caption)
    post_to_instagram(final_path, caption)

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
        top_person = birthdays[0]
        msg = f"🎉 Creating post for {top_person['name']} ({top_person['country']})"
        print(msg)
        send_telegram_alert(msg)
        create_and_post(top_person)
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
    schedule.every().day.at("09:00").do(run_bot)
    schedule.every().day.at("12:00").do(run_bot)
    schedule.every().day.at("18:00").do(run_bot)
    schedule.every().day.at("21:00").do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(30)
