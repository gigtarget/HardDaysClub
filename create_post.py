from PIL import Image, ImageDraw, ImageFont
import os

def create_instagram_post(quote, output_path="output/final_post.png"):
    try:
        width, height = 1080, 1080
        image = Image.new("RGB", (width, height), color="red")
        draw = ImageDraw.Draw(image)

        font_path = "templates/OpenSans-Bold.ttf"
        font_size = 60
        font = ImageFont.truetype(font_path, font_size)

        max_width = width - 100
        lines = []
        words = quote.split()
        while words:
            line = ''
            while words and draw.textlength(line + words[0], font=font) <= max_width:
                line += words.pop(0) + ' '
            lines.append(line.strip())

        total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in lines])
        y = (height - total_text_height) // 2

        for line in lines:
            text_width = draw.textlength(line, font=font)
            x = (width - text_width) // 2
            draw.text((x, y), line, fill="black", font=font)
            y += draw.textbbox((0, 0), line, font=font)[3] + 10

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        print(f"✅ Instagram post created and saved at {output_path}")
        return output_path

    except Exception as e:
        print("❌ Error creating post:", e)
        return None
