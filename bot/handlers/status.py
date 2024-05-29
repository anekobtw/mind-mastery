import time

from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from main import router, start_time


@router.message(F.text, Command("status"))
async def status(message: types.Message, state: FSMContext):
    await message.answer(f"Status: ✅\nUptime: {(time.time() - start_time)} secs")
