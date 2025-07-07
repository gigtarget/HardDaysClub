import csv
import datetime
import os
import schedule
import time
from PIL import Image, ImageDraw, ImageFont

from generate_ai_image import generate_ai_image
from post_to_instagram import post_to_instagram

BIRTHDAY_FILE = "birthdays.csv"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "output"


def load_birthdays(file_path=BIRTHDAY_FILE):
    birthdays = []
    if not os.path.exists(file_path):
        return birthdays
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            birthdays.append(row)
    return birthdays


def get_today_birthdays(birthdays):
    today = datetime.datetime.utcnow().strftime("%m-%d")
    todays = [b for b in birthdays if b["date"] == today]
    return sorted(todays, key=lambda x: int(x.get("popularity", 0)), reverse=True)


# Simple zodiac sign lookup
ZODIAC_RANGES = [
    ((1, 20), "♑"),  # Capricorn until Jan 20
    ((2, 18), "♒"),  # Aquarius until Feb 18
    ((3, 20), "♓"),  # Pisces until Mar 20
    ((4, 20), "♈"),  # Aries until Apr 20
    ((5, 21), "♉"),  # Taurus until May 21
    ((6, 21), "♊"),  # Gemini until Jun 21
    ((7, 22), "♋"),  # Cancer until Jul 22
    ((8, 23), "♌"),  # Leo until Aug 23
    ((9, 23), "♍"),  # Virgo until Sep 23
    ((10, 23), "♎"), # Libra until Oct 23
    ((11, 22), "♏"), # Scorpio until Nov 22
    ((12, 21), "♐"), # Sagittarius until Dec 21
    ((12, 31), "♑"), # Capricorn remainder
]


def get_zodiac_symbol(month, day):
    for (end_month, end_day), symbol in ZODIAC_RANGES:
        if (month < end_month) or (month == end_month and day <= end_day):
            return symbol
    return ""


def compose_birthday_image(name, country, zodiac, base_image, output_path):
    image = Image.open(base_image).convert("RGBA")
    draw = ImageDraw.Draw(image)

    font_path = os.path.join(TEMPLATES_DIR, "OpenSans-Bold.ttf")
    font = ImageFont.truetype(font_path, 80)

    text = f"HAPPY BIRTHDAY {name.upper()}"
    text_w, text_h = draw.textsize(text, font=font)
    x = (image.width - text_w) // 2
    y = image.height - text_h - 40
    draw.text((x, y), text, font=font, fill="white")

    draw.text((40, 40), zodiac, font=font, fill="white")
    draw.text((image.width - 200, 40), country.upper(), font=font, fill="white")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.convert("RGB").save(output_path)
    return output_path


def create_and_post(person):
    name = person["name"]
    country = person["country"]
    month, day = map(int, person["date"].split("-"))
    zodiac = get_zodiac_symbol(month, day)

    ai_path = generate_ai_image(
        f"portrait of {name} in a cinematic, warmly lit style",
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
    post_to_instagram(final_path, caption)


def run_bot():
    birthdays = load_birthdays()
    todays = get_today_birthdays(birthdays)
    if not todays:
        print("No notable birthdays today.")
        return
    top_person = todays[0]
    create_and_post(top_person)


schedule.every().day.at("09:00").do(run_bot)
schedule.every().day.at("12:00").do(run_bot)
schedule.every().day.at("18:00").do(run_bot)
schedule.every().day.at("21:00").do(run_bot)

print("Birthday bot running...")
while True:
    schedule.run_pending()
    time.sleep(30)
