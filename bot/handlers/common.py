import time
from datetime import datetime

import pytz
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dateutil import tz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from database import SettingsManager
from keyboards import confirm_keyboard

router = Router()
sm = SettingsManager()
geolocator = Nominatim(user_agent="anekobtw")
tzfinder = TimezoneFinder()

start_text = (
    "Hey! Welcome to your study buddy. Let's maximize your learning experience with some effective strategies. Below, you'll find a comprehensive list of commands:\n\n",
    "<b>Notes</b>\n",
    "/take_note - Create a new note\n",
    "/notes - Return a list of your notes\n\n",
    "<b>Routine</b>\n",
    "/create_routine - \n",
    "/edit_routine - ",
)


class SettingsForm(StatesGroup):
    location = State()
    time = State()


def get_tz_text(*, location: str = None, approximate_time: str = None) -> tuple[tuple[str], str]:
    # getting timezone
    if location:
        loc = geolocator.geocode(location)
        time.sleep(1)  # in order not to get a ban
        timezone = tz.gettz(tzfinder.timezone_at(lng=loc.longitude, lat=loc.latitude))

    if approximate_time:
        timezone = get_timezone_from_time(approximate_time)

    # getting offset
    offset = get_timezone_offset(timezone)

    return (
        f"Your time zone: <b>GMT{offset}</b>\n",
        f'Your local time: <b>{datetime.now(tz=timezone).strftime("%d %b %Y %H:%M:%S")}</b>\n\n',
        "If that is correct, please press ✅ button. Otherwise, press ❌ button\n",
        "If you don't press anything, this time zone will be used.",
    ), offset


def get_timezone_from_time(approximate_time: str) -> str | None:
    time_zones = pytz.all_timezones
    for time_zone in time_zones:
        local_time = datetime.now(tz=pytz.timezone(time_zone))
        if local_time.strftime("%H:%M") == approximate_time:
            return time_zone
    return None


def get_timezone_offset(timezone) -> str:
    # Get UTC offset in hours and minutes
    offset = datetime.now(pytz.utc).astimezone(timezone).strftime("%z")
    offset_hours = int(offset[:-2])
    offset_minutes = int(offset[-2:])
    offset_str = f"{offset_hours:+d}"
    if offset_minutes:
        offset_str += f":{offset_minutes:02d}"
    return offset_str


@router.message(F.text, Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Canceled.", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text, Command("start"))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    if sm.get_user_settings(message.from_user.id) is None:
        await state.set_state(SettingsForm.location)
        await message.answer(text="Please send me your country or city first so I can identify out your time zone.")
    else:
        await message.answer("".join(start_text))


@router.message(SettingsForm.location)
async def process_location(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    try:
        text, offset = get_tz_text(location=message.text)
        sm.insert_settings(message.from_user.id, offset)
        await message.answer(text="".join(text), reply_markup=confirm_keyboard("start"))
    except Exception:
        await message.answer(f"Something went wrong. Please try again.")
        await state.set_state(SettingsForm.location)


@router.callback_query(F.data == "confirm_start")
async def confirmed(callback: types.CallbackQuery):
    await callback.message.edit_text("".join(start_text))


@router.callback_query(F.data == "refute_start")
async def confirmed(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingsForm.time)
    await callback.message.edit_text("Please send me your time in the following format: XX:XX.\n Type /cancel if you changed your mind.")


@router.message(SettingsForm.time)
async def process_time(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    try:
        text, offset = get_tz_text(approximate_time=message.text)
        sm.delete_settings(message.from_user.id)
        sm.insert_settings(message.from_user.id, offset)
        await message.answer(text="".join(text), reply_markup=confirm_keyboard("start"))
    except Exception:
        await message.answer(f"Something went wrong. Please try again.")
        await state.set_state(SettingsForm.time)
