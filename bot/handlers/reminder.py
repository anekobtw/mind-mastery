from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import ReminderManager
from handlers.common import router

rm = ReminderManager()


class ReminderForm(StatesGroup):
    purpose = State()
    time = State()
    frequency = State()


async def get_message(ftext: str, state: FSMContext):
    user_data = await state.get_data()
    purpose = user_data.get("purpose", "")
    time = user_data.get("time", "")
    frequency = user_data.get("frequency", "")
    message = user_data.get("message", types.Message)

    return (
        f"{ftext}\n\n",
        f"<b>Purpose:</b> {purpose}\n",
        f"<b>Time:</b> {time}\n",
        f"<b>Frequency</b> {frequency}\n\n",
        "Type /cancel if you changed your mind.\n",
    ), message


# Creaing one...
@router.message(F.text, Command("create_reminder"))
async def create_reminder(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ReminderForm.purpose)
    text, _ = await get_message("What do you want me to remind you of?", state)
    message = await message.answer(text="".join(text))
    await state.update_data(message=message)


@router.message(ReminderForm.purpose)
async def process_purpose(message: types.Message, state: FSMContext) -> None:
    await state.update_data(purpose=message.text)
    await state.set_state(ReminderForm.time)
    text, msg = await get_message("When do you want me to remind you?", state)
    await msg.edit_text(text="".join(text))


@router.message(ReminderForm.time)
async def process_time(message: types.Message, state: FSMContext) -> None:
    await state.update_data(time=message.text)
    await state.set_state(ReminderForm.frequency)
    text, msg = await get_message("How often do you want me to remind you?", state)
    await msg.edit_text(text="".join(text))


@router.message(ReminderForm.frequency)
async def process_frequency(message: types.Message, state: FSMContext) -> None:
    await state.update_data(frequency=message.text)
    text, msg = await get_message(
        "If everything is correct, type /confirm_reminder to create the reminder.",
        state,
    )
    await msg.edit_text(text="".join(text))
    await state.set_state(None)


@router.message(F.text, Command("confirm_reminder"))
async def confirm_reminder(message: types.Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    rm.create_reminder(
        user_id=message.from_user.id,
        purpose=user_data["purpose"],
        time=user_data["time"],
        frequency=user_data["frequency"],
    )
    await state.clear()
    await message.answer(text="Reminder created! ✅\nType /reminders to view all reminders.")


@router.message(Command("reminders"))
async def reminders(message: types.Message) -> None:
    ...
