import openai
import config
from telegram_alert import send_error_report

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

def generate_headline_and_caption(news_summary):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a skilled Instagram news editor."},
                {"role": "user", "content": f"""
News: {news_summary}

Create:
1. A short, catchy HEADLINE (max 10 words) – no hashtags
2. A 2–3 line Instagram caption with emojis + relevant hashtags

Format it exactly like:
**Headline:** ...
**Instagram Caption:** ...
"""}
            ],
            temperature=0.7
        )

        full_reply = response.choices[0].message.content
        headline = full_reply.split("**Instagram Caption:**")[0].replace("**Headline:**", "").strip()
        caption = full_reply.split("**Instagram Caption:**")[1].strip()
        return headline, caption

    except Exception as e:
        print("❌ Error generating headline and caption:", e)
        send_error_report("Error generating headline", e)
        return "Breaking News", "📰 Stay tuned for more updates."
