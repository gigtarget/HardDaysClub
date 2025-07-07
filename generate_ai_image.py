import os
import requests
import openai
import config
from telegram_alert import send_telegram_alert, send_telegram_photo

openai.api_key = config.OPENAI_API_KEY


def generate_ai_image(name: str, output_path: str = "output/ai_image.png") -> str:
    """Generate a cinematic portrait of the given person using OpenAI's image API."""
    prompt = (
        f"ultra realistic cinematic portrait of {name}, confident expression, "
        "warmly lit with a soft stage-like background"
    )
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(img_data)
        msg = f"✅ AI Image saved to {output_path}"
        print(msg)
        send_telegram_alert(msg)
        send_telegram_photo(output_path)
        return output_path
    except Exception as e:
        err = f"❌ Error generating image: {e}"
        print(err)
        send_telegram_alert(err)
        return ""
