from PIL import Image, ImageDraw, ImageFont
import os

def create_instagram_post(image_path, headline, output_path="output/final_post.png"):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        font_path = "templates/OpenSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 48)

        text_width, text_height = draw.textbbox((0,0), headline, font=font)[2:4]
        position = ((image.width - text_width) / 2, 30)

        background_width = text_width + 60
        background_height = text_height + 40
        background_position = ((image.width - background_width) / 2, 20)
        
        draw.rectangle(
            [background_position, (background_position[0] + background_width, background_position[1] + background_height)],
            fill=(0, 0, 0, 190)
        )

        draw.text(position, headline, fill="white", font=font)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        print(f"✅ Instagram post created and saved at {output_path}")

        return output_path

    except Exception as e:
        print("❌ Error creating post:", e)
        return None
