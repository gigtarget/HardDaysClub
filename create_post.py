from PIL import Image, ImageDraw, ImageFont
import os
from telegram_alert import send_error_report

def create_instagram_post(quote, output_path="output/final_post.png"):
    try:
        width, height = 1080, 1350
        padding = 100
        max_width = width - 2 * padding

        # Set black background
        image = Image.new("RGB", (width, height), color="#000000")
        draw = ImageDraw.Draw(image)

        # Use Playfair Display font
        font_path = "templates/PlayfairDisplay-VariableFont_wght.ttf"
        font_size = 72

        while font_size > 20:
            font = ImageFont.truetype(font_path, font_size)
            words = quote.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if draw.textlength(test_line, font=font) <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())

            total_height = sum(
                [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
            ) + (len(lines) - 1) * 10

            if total_height <= height - 2 * padding:
                break
            font_size -= 2

        # Center block vertically
        y = (height - total_height) // 2

        for line in lines:
            draw.text((padding, y), line, font=font, fill="#FFFFFF")  # White text
            y += draw.textbbox((0, 0), line, font=font)[3] + 10

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        print(f"✅ Styled quote image saved to {output_path}")
        return output_path

    except Exception as e:
        print("❌ Error creating image:", e)
        send_error_report("Error creating image", e)
        return None
