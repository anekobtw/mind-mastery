import time

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from main import start_time

router = Router()


@router.message(F.text, Command("status", "uptime"))
async def status(message: types.Message, state: FSMContext):
    await message.answer(f"Status: ✅\nUptime: {(time.time() - start_time)} secs")
