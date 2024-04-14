from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import ReminderManager, SettingsManager
from handlers.common import router
from keyboards import confirm_keyboard, get_nums_kb
from misc import datetime_to_utc_timestamp, parse_datetime

rm = ReminderManager()
sm = SettingsManager()


class ReminderForm(StatesGroup):
    purpose = State()
    time = State()
    frequency = State()


async def update_message(ftext: str, state: FSMContext, reply_markup: types.InlineKeyboardMarkup = None) -> None:
    user_data = await state.get_data()
    purpose = user_data.get("purpose", "")
    time = user_data.get("time", "")
    frequency = user_data.get("frequency", "")
    message = user_data.get("message", types.Message)

    text = (
        f"{ftext}\n\n",
        f"<b>Purpose:</b> {purpose}\n",
        f"<b>Time:</b> {time}\n",
        f"<b>Frequency:</b> {frequency}\n\n",
        "Type /cancel if you changed your mind.\n",
    )
    await message.edit_text(text="".join(text), reply_markup=reply_markup)


# Creaing one...
@router.message(F.text, Command("create_reminder"))
async def create_reminder(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ReminderForm.purpose)
    message = await message.answer("What do you want me to remind you of?")
    await state.update_data(message=message)
    await state.update_data(user_id=message.from_user.id)


@router.message(ReminderForm.purpose)
async def process_purpose(message: types.Message, state: FSMContext) -> None:
    await state.update_data(purpose=message.text)
    await state.set_state(ReminderForm.time)
    await update_message("When do you want me to remind you?", state)


@router.message(ReminderForm.time)
async def process_time(message: types.Message, state: FSMContext) -> None:
    datetime = parse_datetime(message.text)
    await state.update_data(time=datetime.strftime("%d %b %Y %H:%M:%S"))
    await state.update_data(timestamp=datetime_to_utc_timestamp(datetime))
    await state.set_state(ReminderForm.frequency)
    await update_message("How often do you want me to remind you?", state)


@router.message(ReminderForm.frequency)
async def process_frequency(message: types.Message, state: FSMContext) -> None:
    await state.update_data(frequency=message.text)
    await update_message("If everything is correct, press ✅ to create the reminder.", state, confirm_keyboard("reminder"))
    await state.set_state(None)


@router.callback_query(F.data == "confirm_reminder")
async def confirmed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    rm.create_reminder(
        user_id=user_data["user_id"],
        purpose=user_data["purpose"],
        timestamp=user_data["timestamp"],
        frequency=user_data["frequency"],
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

    if reminders_list is None:
        await message.answer("You don't have any reminders yet.")
    else:
        reminders = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(reminders_list)])
        await message.answer(text=reminders, reply_markup=get_nums_kb(reminders_list, "reminder"))


# @router.callback_query(F.data.startswith("note_info_"))
# async def note_info(callback: types.CallbackQuery):
#     note = nm.get_note_info(note_id=callback.data.split("_")[2])

#     text = (
#         f"<b>ID in database:</b> {note[0]}\n",
#         f"<b>Author Telegram ID:</b> {note[1]}\n",
#         f"<b>Text:</b> {note[2]}\n",
#     )

#     await callback.message.edit_text("".join(text), reply_markup=get_delete_keyboard(note))
