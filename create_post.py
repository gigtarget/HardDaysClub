from PIL import Image, ImageDraw, ImageFont
import os

def create_styled_instagram_post(quote, output_path="output/final_post.png"):
    try:
        width, height = 1080, 1350
        padding = 100
        max_width = width - 2 * padding

        # Black background
        image = Image.new("RGB", (width, height), color="#000000")
        draw = ImageDraw.Draw(image)

        # Font path
        font_path = "templates/PlayfairDisplay-VariableFont_wght.ttf"
        font_size = 72

        # Strong words to highlight in red
        strong_words = {
            "fight", "rise", "struggle", "win", "power", "believe", "never", "always",
            "truth", "courage", "dream", "focus", "hustle", "grind", "fearless", "strength"
        }

        # Load font with fallback
        def safe_font(path, size):
            try:
                return ImageFont.truetype(path, size)
            except:
                return ImageFont.load_default()

        while font_size > 20:
            font = safe_font(font_path, font_size)
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

        y = (height - total_height) // 2

        for line in lines:
            x = padding
            for word in line.split():
                word_with_space = word + " "
                color = "#ff4444" if word.lower().strip(",.!?") in strong_words else "#ffffff"
                draw.text((x, y), word_with_space, font=font, fill=color)
                x += draw.textlength(word_with_space, font=font)
            y += draw.textbbox((0, 0), line, font=font)[3] + 10

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        print(f"✅ Quote image saved to: {output_path}")
        return output_path

    except Exception as e:
        print("❌ Error creating image:", e)
        return None
