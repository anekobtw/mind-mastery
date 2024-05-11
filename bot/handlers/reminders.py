import os
import time
from datetime import datetime, timedelta

from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dateutil import parser
from dotenv import load_dotenv

from database import ReminderManager, SettingsManager
from keyboards import confirm_keyboard, get_delete_keyboard, list_to_kb
from main import router

rm = ReminderManager()
sm = SettingsManager()


class ReminderForm(StatesGroup):
    purpose = State()
    time = State()


text = "{}\n\n<b>Purpose:</b> {}\n<b>Time:</b> {}\n\nType /cancel if you changed your mind."


# Creaing one...
@router.message(F.text, Command("create_reminder"))
async def create_reminder(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ReminderForm.purpose)
    msg = await message.answer(text.format("What do you want me to remind you of?", "___", "___"))
    await state.update_data(message=msg)


@router.message(ReminderForm.purpose)
async def process_purpose(message: types.Message, state: FSMContext) -> None:
    await state.update_data(purpose=message.text)
    await state.set_state(ReminderForm.time)
    user_data = await state.get_data()
    await user_data.get("message").edit_text(text.format("When do you want me to remind you?", user_data.get("purpose"), "___"))


@router.message(ReminderForm.time)
async def process_time(message: types.Message, state: FSMContext) -> None:
    try:
        load_dotenv()
        local_datetime = parser.parse(message.text, fuzzy=True)
        adjusted_datetime = (
            local_datetime
            + timedelta(seconds=int(os.getenv("MY_TIMEZONE_AHEAD_SECONDS")))
            - timedelta(seconds=sm.get_user_settings(message.from_user.id)[1])
        )

        user_data = await state.get_data()
        await user_data.get("message").edit_text(
            text.format(
                "If everything is correct, press ✅ to create the reminder.", user_data.get("purpose"), local_datetime.strftime("%d %b %Y %H:%M:%S")
            ),
            reply_markup=confirm_keyboard("reminder"),
        )

        await state.update_data(utc_timestamp=int(adjusted_datetime.timestamp()))
        await state.update_data(local_timestamp=int(local_datetime.timestamp()))
        await state.set_state(None)
    except:
        user_data = await state.get_data()
        await user_data.get("message").edit_text(
            text.format(
                "When do you want me to remind you?\nTry writing the time like this:\nday month year time (for example 25 june 2024 15:35)",
                user_data.get("purpose"),
                "___",
            ),
            reply_markup=confirm_keyboard("reminder"),
        )
        await state.set_state(ReminderForm.time)


@router.callback_query(F.data == "confirm_reminder")
async def confirmed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    rm.create_reminder(
        user_id=callback.from_user.id,
        purpose=user_data["purpose"],
        utc_timestamp=user_data["utc_timestamp"],
        local_timestamp=user_data["local_timestamp"],
    )
    await state.clear()
    await callback.message.answer(text="Reminder created! ✅\nType /reminders to view all reminders.")


@router.callback_query(F.data == "refute_reminder")
async def refuted(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Canceled.")


# Editing
@router.message(F.text, Command("reminders"))
async def reminders(message: types.Message) -> None:
    list_of_reminders = rm.get_user_reminders(message.from_user.id)

    if list_of_reminders:
        reminders = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(list_of_reminders)])
        await message.answer(text=reminders, reply_markup=list_to_kb(list_of_reminders, "reminder"))
    else:
        await message.answer("You don't have any reminders yet.\nType /create_reminder to create one.")


@router.callback_query(F.data.startswith("reminder_info_"))
async def note_info(callback: types.CallbackQuery):
    reminder = rm.get_reminder_info(reminder_id=callback.data.split("_")[2])
    reminder_time = datetime.fromtimestamp(reminder[4])

    text = (
        f"<b>Purpose:</b> {reminder[2]}\n",
        f"<b>Time:</b> {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}\n",
    )

    await callback.message.edit_text("".join(text), reply_markup=get_delete_keyboard(reminder[0], "reminder"))


@router.callback_query(F.data.startswith("delete_reminder_"))
async def delete_reminder(callback: types.CallbackQuery):
    action = callback.data.split("_")[2]

    if action != "cancel":
        rm.delete_reminder(int(action))
        await callback.message.edit_text(text="Deleted successfully! ✅")
        time.sleep(0.5)

    list_of_reminders = rm.get_user_reminders(callback.from_user.id)
    reminders = "\n".join([f"<b>{ind+1}.</b> {reminder[2]}\n" for ind, reminder in enumerate(list_of_reminders)])
    if reminders:
        await callback.message.edit_text(text=reminders, reply_markup=list_to_kb(list_of_reminders, "reminder"))
    else:
        await callback.message.edit_text(text="You don't have any reminders yet.\nType /create_reminder to create one.")
