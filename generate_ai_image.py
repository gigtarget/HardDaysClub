import os
import base64
from openai import OpenAI
import config
from telegram_alert import send_telegram_alert, send_telegram_photo

client = OpenAI(api_key=config.OPENAI_API_KEY)


def generate_ai_image(name: str, country: str, zodiac: str, output_path: str = "output/ai_image.png") -> str:
    """Generate a full birthday image using GPT Image."""
    prompt = (
        f"Ultra-realistic high-resolution full-body portrait of {name}, 3/4th of upper body standing confidently on a softly lit stage with a dark gradient or black background. "
        f"The person is smiling or appearing calm and composed, dressed in his/her famous attire. The overall aesthetic is cinematic, clean, and respectful.\n\n"
        "Ensure the image has extra space at the bottom reserved for text.\n"
        f"At the bottom center, clearly add large, bold text:\nHAPPY BIRTHDAY\n{name}\n\n"
        f"Below the text, place symmetrical zodiac symbols: one {zodiac} on the left and one on the right. In the center, add a stylish icon representing {country}.\n\n"
        "The image should be sized exactly 1080x1080 pixels for Instagram, with proper spacing to prevent any cropping. "
        "It should resemble a professionally lit award show photo or magazine cover. Use soft shadows and elegant composition."
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
