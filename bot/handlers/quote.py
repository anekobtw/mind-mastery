import os
import textwrap

import pyquotegen
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from PIL import Image, ImageDraw, ImageFont

from keyboards import quotes_keyboard

router = Router()


@router.message(F.text, Command("quote"))
async def quote_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Please, choose an option.", reply_markup=quotes_keyboard())


@router.callback_query(F.data.startswith("quote_"))
async def send_quote(callback: types.CallbackQuery):
    quote = pyquotegen.get_quote(callback.data.split("_")[1])

    image = Image.open("assets/quote.png")
    draw = ImageDraw.Draw(image)
    text = textwrap.fill(quote, width=50)
    font = ImageFont.truetype("assets/AbrilFatface-Regular.ttf", 52.6)

    _, _, text_width, text_height = draw.textbbox(xy=(0, 250), text=text, font=font)
    text_x = (image.width - text_width) / 2
    text_y = (image.height - text_height) / 2
    draw.text((text_x, text_y), text, fill="#292929", font=font)

    image.save("assets/quote1.png")
    image.close()
    await callback.message.delete()
    await callback.message.answer_photo(types.FSInputFile("assets/quote1.png"))
    os.remove("assets/quote1.png")
