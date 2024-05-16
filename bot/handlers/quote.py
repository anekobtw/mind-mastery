import textwrap

from aiogram import F, types
from aiogram.filters import Command
from inspirational_quotes import quote
from PIL import Image, ImageDraw, ImageFont

from main import router


@router.message(F.text, Command("quote"))
async def quote_command(message: types.Message) -> None:
    # generating til i can find a quite short one
    quote_to_send = quote()
    while len(quote_to_send["quote"]) > 125:
        quote_to_send = quote()

    # properties of a pic
    image = Image.open("quote.png")
    draw = ImageDraw.Draw(image)
    raw_text = '"' + quote_to_send["quote"] + '"' + " (c) " + quote_to_send["author"]
    text = textwrap.fill(raw_text, width=50)
    font = ImageFont.truetype("AbrilFatface-Regular.ttf", 52.6)

    # trying to make the text in the middle
    _, _, text_width, text_height = draw.textbbox(xy=(0, 250), text=text, font=font)
    text_x = (image.width - text_width) / 2
    text_y = (image.height - text_height) / 2

    # sending
    draw.text((text_x, text_y), text, fill="#292929", font=font)
    image.save("quote1.png")
    await message.answer_photo(types.FSInputFile("quote1.png"))
