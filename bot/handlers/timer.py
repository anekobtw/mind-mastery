from aiogram import F, types
from aiogram.filters import Command

from keyboards import website_button
from main import router

web_app_info = types.WebAppInfo(url="https://pomofocus.io/")


@router.message(F.text, Command("timer"))
async def timer(message: types.Message) -> None:
    await message.answer("I highly recommend you <b>pomofocus</b> website.", reply_markup=website_button(web_app_info))
