import random
import openai
import psycopg2
from config import DATABASE_URL, OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

PREDEFINED_QUOTES = [
    "What lies behind us are small matters. – Emerson",
    "Do or do not. There is no try. – Yoda",
    "It always seems impossible until it's done. – Nelson Mandela",
    "Fortune favors the brave. – Terence",
    "Action is the foundational key to success. – Picasso",
    "Fall seven times, stand up eight. – Japanese Proverb",
    "No pressure, no diamonds. – Thomas Carlyle",
    "The harder the battle, the sweeter the victory. – Les Brown",
    "Pain is temporary, quitting lasts forever. – Lance Armstrong",
    "Tough times never last. Tough people do. – Robert Schuller",
    "Success is walking from failure to failure. – Winston Churchill",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "He who has a why can endure any how. – Nietzsche",
    "Don't count the days. Make the days count. – Muhammad Ali",
    "Everything you can imagine is real. – Pablo Picasso",
    "If you’re going through hell, keep going. – Winston Churchill",
    "Courage is grace under pressure. – Ernest Hemingway",
    "The best revenge is massive success. – Frank Sinatra",
    "Dream big. Dare bigger. – Norman Vaughan",
    "Life begins at the end of comfort. – Neale Donald Walsch",
    "Hard choices, easy life. – Jerzy Gregorek",
    "Success is a series of small wins. – Unknown",
    "Screw it, let's do it. – Richard Branson",
    "Stay hungry. Stay foolish. – Steve Jobs",
    "Work hard in silence. – Frank Ocean",
    "Discipline equals freedom. – Jocko Willink",
    "Be yourself. Everyone else is taken. – Oscar Wilde",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "Make each day your masterpiece. – John Wooden",
    "Act as if it were impossible to fail. – Dorothea Brande",
    "Success demands sacrifice. – Unknown",
    "Be so good they can’t ignore you. – Steve Martin",
    "Do one thing every day that scares you. – Eleanor Roosevelt",
    "What you do speaks loudly. – Ralph Waldo Emerson",
    "Fortune sides with him who dares. – Virgil",
    "Courage is resistance to fear. – Mark Twain",
    "Hustle beats talent. – Ross Simmonds",
    "Don’t wish it were easier. – Jim Rohn",
    "You miss 100% of shots not taken. – Wayne Gretzky",
    "Obsessed is a word the lazy use. – Tim Grover",
    "Losers quit when they're tired. – Marilyn Monroe",
    "Don't stop until you're proud. – Unknown",
    "Success is never owned. – Rory Vaden",
    "Do the work others won’t. – Grant Cardone",
    "Doubt kills more dreams than failure. – Suzy Kassem",
    "Talent is cheaper than perseverance. – Stephen King",
    "Effort never betrays you. – Tim Notke",
    "Courage doesn’t always roar. – Mary Anne Radmacher",
    "Don’t let yesterday take too much. – Will Rogers",
    "The struggle you're in today builds strength. – Robert Tew",
    "Grind now, shine later. – Unknown",
    "It’s never too late to begin. – George Eliot",
    "Stay strong, stand up. – LL Cool J",
    "I am not a product of circumstances. – Stephen Covey",
    "Storms make trees take deeper roots. – Dolly Parton",
    "The best way out is always through. – Robert Frost",
    "Let perseverance finish its work. – James 1:4 (Bible)",
    "Be fearless in pursuit. – Jennifer Lee",
    "Excuses are lies we tell ourselves. – Jocko Willink",
    "We suffer more in imagination. – Seneca",
    "Don't wish for it. Work for it. – Unknown",
    "Fall in love with the process. – Eric Thomas",
    "No guts, no story. – Chris Brady",
    "It’s not over until I win. – Les Brown",
    "Take the risk or lose the chance. – Unknown",
    "You don’t find willpower. You create it. – Unknown",
    "We can do hard things. – Glennon Doyle",
    "You only fail when you stop trying. – Albert Einstein",
    "Power is gained by discipline. – Unknown",
    "Greatness is earned, never given. – Unknown",
    "Victory is reserved for the fearless. – Sun Tzu",
    "Strength grows in moments of pain. – Unknown",
    "Fear is a liar. – Zig Ziglar",
    "You define your limits. – Unknown",
    "Be relentless. – Tim Grover",
    "Train hard, fight easy. – Alexander Suvorov",
    "Don't wish for easy. – Bruce Lee",
    "Success is rented, due daily. – Rory Vaden",
    "Pressure reveals character. – Unknown",
    "No one is coming to save you. – David Goggins",
    "Earn it every day. – Jocko Willink",
    "Comfort is a slow death. – Carl Jung",
    "Winners focus on winning. – Conor McGregor",
    "Starve distractions, feed focus. – Unknown",
    "Humble hustle wins. – Gary Vaynerchuk",
    "Don’t stop until it hurts. – Eric Thomas",
    "Turn your pain into power. – Robin Sharma",
    "Your only limit is you. – Unknown",
    "Pain unlocks greatness. – David Goggins",
    "Failure is fuel. – Kobe Bryant",
    "Die with memories, not dreams. – Unknown",
    "You are the storm. – Unknown",
    "Born to stand out. – Dr. Seuss",
    "Don't break, break through. – Unknown",
    "Let your grind talk. – Unknown",
    "Never apologize for ambition. – Unknown",
    "Toughness is in your choices. – Angela Duckworth",
    "There is no finish line. – Nike",
    "Mastery loves boredom. – James Clear",
    "Your mind gives up first. – Unknown"
]

def generate_motivational_quote():
    random.shuffle(PREDEFINED_QUOTES)
    for quote in PREDEFINED_QUOTES:
        if insert_unique_quote_to_db(quote):
            print("✅ Picked unused predefined quote.")
            return quote

    # All quotes used — fallback to GPT
    print("⚠️ All predefined quotes used. Generating new one via OpenAI.")
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
    quote = generate_motivational_quote()
    print("📤 Final Quote:", quote)
    return quote
