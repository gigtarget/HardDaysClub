import os
import base64
from openai import OpenAI
import config
from telegram_alert import send_telegram_alert, send_telegram_photo

client = OpenAI(api_key=config.OPENAI_API_KEY)


def generate_ai_image(name: str, country: str, zodiac: str, output_path: str = "output/ai_image.png") -> str:
    """Generate a full birthday image using GPT Image."""
    prompt = (
        f"Ultra-realistic high-resolution portrait of {name}, standing confidently on a softly lit stage with a dark gradient or black background. "
        f"The person is smiling or appearing calm and composed, wearing formal attire, with a clean and cinematic aesthetic.\n"
        f"Add bold centered text at the bottom that reads:\n'HAPPY BIRTHDAY\n{name}'\n"
        f"Below that, include symmetrical zodiac symbols {zodiac} on the left and right and a stylish center icon representing {country}. "
        "The image should look like a professional stage or award show photo, with soft shadows and magazine cover quality. "
        "Maintain a warm, respectful, and celebratory vibe."
    )

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="high",
        )
        image_base64 = response.data[0].b64_json
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))
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
