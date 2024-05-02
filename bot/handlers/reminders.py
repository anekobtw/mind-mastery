import time
from datetime import datetime

from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import ReminderManager, SettingsManager
from keyboards import confirm_keyboard, get_delete_keyboard, get_nums_kb
from main import router
from misc import parse_datetime

rm = ReminderManager()
sm = SettingsManager()


class ReminderForm(StatesGroup):
    purpose = State()
    time = State()


async def update_message(ftext: str, state: FSMContext, reply_markup: types.InlineKeyboardMarkup = None) -> None:
    user_data = await state.get_data()
    purpose = user_data.get("purpose", "")
    time = user_data.get("time", "")
    message = user_data.get("message", types.Message)

    text = (f"{ftext}\n\n", f"<b>Purpose:</b> {purpose}\n", f"<b>Time:</b> {time}\n\n", "Type /cancel if you changed your mind.")
    await message.edit_text(text="".join(text), reply_markup=reply_markup)


# Creaing one...
@router.message(F.text, Command("create_reminder"))
async def create_reminder(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ReminderForm.purpose)
    msg = await message.answer("What do you want me to remind you of?\n\n<b>Purpose:</b>\n<b>Time:</b>\n\nType /cancel if you changed your mind.")
    await state.update_data(message=msg)


@router.message(ReminderForm.purpose)
async def process_purpose(message: types.Message, state: FSMContext) -> None:
    await state.update_data(purpose=message.text)
    await state.set_state(ReminderForm.time)
    await update_message("When do you want me to remind you?", state)


@router.message(ReminderForm.time)
async def process_time(message: types.Message, state: FSMContext) -> None:
    try:
        local_datetime = parse_datetime(message.text)
        await state.update_data(time=local_datetime.strftime("%d %b %Y %H:%M:%S"))
        await state.update_data(timestamp=int(local_datetime.timestamp()))
        await update_message("If everything is correct, press ✅ to create the reminder.", state, confirm_keyboard("reminder"))
        await state.set_state(None)
    except:
        await update_message(
            "When do you want me to remind you?\nTry writing the time like this:\nday month year time (for example 25 june 2024 15:35)", state
        )
        await state.set_state(ReminderForm.time)


@router.callback_query(F.data == "confirm_reminder")
async def confirmed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    rm.create_reminder(
        user_id=callback.from_user.id,
        purpose=user_data["purpose"],
        timestamp=user_data["timestamp"],
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
    reminders_list = rm.get_user_reminders(message.from_user.id)

    if reminders_list:
        reminders = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(reminders_list)])
        await message.answer(text=reminders, reply_markup=get_nums_kb(reminders_list, "reminder"))
    else:
        await message.answer("You don't have any reminders yet.\nType /create_reminder to create one.")


@router.callback_query(F.data.startswith("reminder_info_"))
async def note_info(callback: types.CallbackQuery):
    reminder = rm.get_reminder_info(reminder_id=callback.data.split("_")[2])
    datetime_obj = datetime.fromtimestamp(reminder[3])

    text = (
        f"<b>Purpose:</b> {reminder[2]}\n",
        f"<b>Time:</b> {datetime_obj.strftime('%Y-%m-%d %H:%M:%S')}\n",
    )

    await callback.message.edit_text("".join(text), reply_markup=get_delete_keyboard(reminder, "reminder"))


@router.callback_query(F.data.startswith("delete_reminder_"))
async def delete_reminder(callback: types.CallbackQuery):
    action = callback.data.split("_")[2]

    if action != "cancel":
        rm.delete_reminder(int(action))
        await callback.message.edit_text(text="Deleted successfully! ✅")
        time.sleep(1)
    reminders_list = rm.get_user_reminders(callback.from_user.id)
    reminders = "\n".join([f"<b>{ind+1}.</b> {reminder[2]}\n" for ind, reminder in enumerate(reminders_list)])
    if reminders:
        await callback.message.edit_text(text=reminders, reply_markup=get_nums_kb(reminders_list, "reminder"))
    else:
        await callback.message.edit_text(text="You don't have any reminders yet.\nType /create_reminder to create one.")
