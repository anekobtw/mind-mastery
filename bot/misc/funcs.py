import textwrap

from PIL import Image, ImageDraw, ImageFont


def generate_image(text: str) -> None:
    image = Image.open("assets/quote.png")
    draw = ImageDraw.Draw(image)
    text = textwrap.fill(text, width=50)
    font = ImageFont.truetype("assets/AbrilFatface-Regular.ttf", 52.6)

    _, _, text_width, text_height = draw.textbbox(xy=(0, 250), text=text, font=font)
    text_x = (image.width - text_width) / 2
    text_y = (image.height - text_height) / 2
    draw.text((text_x, text_y), text, fill="#292929", font=font)

    image.save("assets/quote1.png")
    image.close()
