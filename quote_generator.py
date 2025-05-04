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
                "content": "You are a viral Instagram content creator. You generate short, original, and emotionally powerful motivational quotes tailored for Instagram audience engagement."
            },
            {
                "role": "user",
                "content": "Write a random style of deep, witty, Gen Z, emotional, stoic motivational quote under 10 words that could go viral on Instagram, short and simple not too complicated, simple but strong words."
            }
        ],
        temperature=0.9
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
