from aiogram import F, types
from aiogram.filters import Command

from keyboards import get_reminders_kb
from main import router


@router.message(F.text, Command("create_reminder"))
async def create_reminder(message: types.Message):
    await message.answer("Which timer do you want?", reply_markup=get_reminders_kb())
