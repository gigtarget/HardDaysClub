import openai
import psycopg2
from config import DATABASE_URL, OPENAI_API_KEY

# Use the correct OpenAI client initialization for openai>=1.0.0
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_motivational_quote():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a viral content creator. You write short, powerful, and emotionally resonant quotes for Instagram and social media. Your content is highly relatable, simple, and makes people want to share it instantly with friends, family, or coworkers. Avoid clichés and make sure each quote sounds fresh and human."
            },
            {
                "role": "user",
                "content": "Write a short, powerful, emotionally resonant quote under 12 words that embodies mental toughness, resilience, grit, or determination. It should feel like a punch — minimal words, maximum impact. The tone should be bold, serious, and inspiring — something a person would share during hard times or use as a reminder of their strength. Avoid clichés, don't rhyme, and don’t include any hashtags or emojis."
            }
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

def insert_unique_quote_to_db(quote):
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO quotes (text, used) VALUES (%s, TRUE) ON CONFLICT DO NOTHING RETURNING id;",
            (quote,)
        )
        inserted = cur.fetchone()
        conn.commit()
        return inserted is not None
    finally:
        conn.close()

def generate_and_post_unique_quote():
    for _ in range(5):
        quote = generate_motivational_quote()
        if insert_unique_quote_to_db(quote):
            print("✅ New quote added and marked as used.")
            return quote
        print("⚠️ Duplicate quote, regenerating...")

    raise Exception("❌ Could not generate a unique quote after multiple attempts.")
