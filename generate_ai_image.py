import openai
import config
import requests
import os

openai.api_key = config.OPENAI_API_KEY

def generate_ai_image(prompt, output_path="output/ai_image.png"):
    try:
        # Step 1: Use ChatGPT to prepare the prompt intelligently
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a prompt enhancer that rewrites prompts for generating high-quality cinematic images."
                },
                {
                    "role": "user",
                    "content": f"Generate a prompt for: '{prompt}'"
                }
            ],
            tools=[{"type": "image_generation"}],
            tool_choice={"type": "image_generation"}
        )

        # Step 2: Extract the image URL
        image_url = response["tool_calls"][0]["image_generation"]["url"]

        # Step 3: Download the image
        img_data = requests.get(image_url).content
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as handler:
            handler.write(img_data)

        print(f"✅ AI Image generated and saved at {output_path}")
        return output_path

    except Exception as e:
        print("❌ Error generating image:", e)
        return None
