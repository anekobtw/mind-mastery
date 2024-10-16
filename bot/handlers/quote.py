import os

import pyquotegen
import requests
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import quotes_keyboard
from misc.funcs import generate_image

router = Router()


@router.message(F.text, Command("quote"))
async def quote_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Please, choose an option.", reply_markup=quotes_keyboard())


@router.callback_query(F.data.startswith("quote_"))
async def send_quote(callback: types.CallbackQuery):
    generate_image(pyquotegen.get_quote(callback.data.split("_")[1]))
    await callback.message.delete()
    await callback.message.answer_photo(types.FSInputFile("assets/quote1.png"))
    os.remove("assets/quote1.png")


@router.message(F.text, Command("affirmation"))
async def quote_command(message: types.Message, state: FSMContext):
    await state.clear()
    response = requests.get("https://www.affirmations.dev/")
    generate_image(response.json()["affirmation"])
    await message.answer_photo(types.FSInputFile("assets/quote1.png"))
    os.remove("assets/quote1.png")
