import openai
import psycopg2
from config import DATABASE_URL, OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_motivational_quote():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a motivational quote generator."},
            {"role": "user", "content": "Give me one short original motivational quote (no duplicates)."}
        ],
        temperature=0.9
    )
    return response.choices[0].message.content.strip()
