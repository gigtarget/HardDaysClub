import sqlite3
import os

DB_PATH = "quotes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT UNIQUE,
        used INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_quotes_from_file(file_path="quotes.csv"):
    if not os.path.exists(file_path):
        print("❌ quotes.csv not found.")
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            quote = line.strip()
            if quote:
                try:
                    cursor.execute("INSERT INTO quotes (text) VALUES (?)", (quote,))
                except sqlite3.IntegrityError:
                    continue
    conn.commit()
    conn.close()

def get_random_unused_quote():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM quotes WHERE used = 0 ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result  # returns (id, text)

def mark_quote_as_used(quote_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE quotes SET used = 1 WHERE id = ?", (quote_id,))
    conn.commit()
    conn.close()
