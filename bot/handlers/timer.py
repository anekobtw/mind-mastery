from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import website_button
from main import router


@router.message(F.text, Command("timer"))
async def timer(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "I highly recommend you <b>pomofocus</b> website.",
        reply_markup=website_button(
            "Open pomofocus", types.WebAppInfo(url="https://pomofocus.io/")
        ),
    )
