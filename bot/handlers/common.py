from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import SettingsManager
from keyboards import confirm_keyboard
from main import router
from misc import get_tz_text, start_text

sm = SettingsManager()


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


@router.message(F.text, Command("change_timezone"))
async def change_timezone(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(SettingsForm.location)
    await message.answer(
        text="Please, send me your country or city first so I can identify your time zone."
    )


@router.message(F.text, Command("start", "help"))
async def start_command_handler(message: types.Message, state: FSMContext):
    await state.clear()
    if sm.get_user_settings(message.from_user.id) is None:
        await state.set_state(SettingsForm.location)
        await message.answer(
            text="Please, send me your country or city first so I can identify your time zone."
        )
    else:
        await message.answer(start_text)


@router.message(SettingsForm.location)
async def process_location(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        text, offset_secs = get_tz_text(location=message.text)
        if sm.get_user_settings(message.from_user.id) is not None:
            sm.delete_settings(message.from_user.id)
        sm.create_settings(message.from_user.id, offset_secs)
        await message.answer(text="".join(text), reply_markup=confirm_keyboard("start"))
    except Exception:
        await message.answer(
            "Something went wrong. Send me your time in the following format: XX:XX."
        )
        await state.set_state(SettingsForm.time)


@router.callback_query(F.data == "confirm_start")
async def confirmed(callback: types.CallbackQuery):
    await callback.message.edit_text("".join(start_text))


@router.callback_query(F.data == "refute_start")
async def refuted(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SettingsForm.time)
    await callback.message.edit_text("Then send me your time in the following format: XX:XX.")


@router.message(SettingsForm.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        text, offset_secs = get_tz_text(approximate_time=message.text)
        sm.delete_settings(message.from_user.id)
        sm.create_settings(message.from_user.id, offset_secs)
        await message.answer(text="".join(text), reply_markup=confirm_keyboard("start"))
    except Exception:
        await message.answer(f"Something went wrong. Please try again.")
        await state.set_state(SettingsForm.time)


@router.message(F.text, Command("links"))
async def links(message: types.Message, state: FSMContext):
    await state.clear()
    txt = """
Developer: @anekobtw

Developer's channel: @anekobtww

Source code of the bot: https://github.com/anekobtw/mind-mastery
"""
    await message.answer(txt)
