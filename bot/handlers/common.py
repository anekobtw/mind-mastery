from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from main import router
from misc import start_text


class SettingsForm(StatesGroup):
    location = State()
    time = State()


@router.message(F.text, Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Canceled.", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text, Command("start", "help"))
async def start_command_handler(message: types.Message, state: FSMContext):
    await message.answer(start_text)


@router.message(F.text, Command("links"))
async def links(message: types.Message, state: FSMContext):
    await state.clear()
    txt = """
Developer: @anekobtw

Developer's channel: @anekobtww

Source code of the bot: https://github.com/anekobtw/mind-mastery
"""
    await message.answer(txt)
