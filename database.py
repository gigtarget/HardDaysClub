import psycopg2
import os
from config import DATABASE_URL

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            text TEXT UNIQUE,
            used BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    conn.close()

def add_quotes_from_file(file_path="quotes.csv"):
    if not os.path.exists(file_path):
        print("❌ quotes.csv not found.")
        return

    conn = get_conn()
    cur = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            quote = line.strip()
            if quote:
                try:
                    cur.execute("INSERT INTO quotes (text) VALUES (%s) ON CONFLICT DO NOTHING", (quote,))
                except Exception as e:
                    print("⚠️ Error adding quote:", e)
    conn.commit()
    conn.close()

def get_random_unused_quote():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM quotes WHERE used = FALSE ORDER BY RANDOM() LIMIT 1")
    result = cur.fetchone()
    conn.close()
    return result

def mark_quote_as_used(quote_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE quotes SET used = TRUE WHERE id = %s", (quote_id,))
    conn.commit()
    conn.close()
