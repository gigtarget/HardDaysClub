import openai
import psycopg2
from config import DATABASE_URL, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_motivational_quote():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a motivational quote generator."},
            {"role": "user", "content": "Give me one short original motivational quote (no duplicates)."}
        ],
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def insert_unique_quote_to_db(quote):
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO quotes (text, used) VALUES (%s, TRUE) ON CONFLICT DO NOTHING RETURNING id;", (quote,))
        inserted = cur.fetchone()
        conn.commit()
        return inserted is not None
    finally:
        conn.close()

def generate_and_post_unique_quote():
    for _ in range(5):  # Try up to 5 times
        quote = generate_motivational_quote()
        if insert_unique_quote_to_db(quote):
            print("✅ New quote added and marked as used.")
            return quote
        print("⚠️ Duplicate quote, regenerating...")

    raise Exception("❌ Could not generate a unique quote after multiple attempts.")
