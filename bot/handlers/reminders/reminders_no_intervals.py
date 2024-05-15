from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import RNIManager
from keyboards import confirm_keyboard
from main import router
from misc import local_to_utc


class RNIForm(StatesGroup):
    purpose = State()
    time = State()


@router.callback_query(F.data == "without_intervals")
async def without_intervals(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Okay, let's create one without intervals. Remember that you can type /cancel at any time if you change your mind.")
    msg = await callback.message.answer("What do you want me to remind you of?")
    await state.update_data(message=msg)
    await state.set_state(RNIForm.purpose)


@router.message(RNIForm.purpose)
async def process_purpose(message: types.Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    user_data = await state.get_data()
    await user_data.get("message").edit_text("When do you want me to remind you?")
    await state.set_state(RNIForm.time)


@router.message(RNIForm.time)
async def process_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        txt = f"""
Check everything and confirm creating by pressing ✅ button below.

<b>Purpose:</b> {user_data.get("purpose")}
<b>Time:</b> {local_to_utc(message, False)[0].strftime("%d %b %Y %H:%M:%S")}
"""
        await user_data.get("message").edit_text(txt, reply_markup=confirm_keyboard("rni"))
        await state.update_data(utc_timestamp=int(local_to_utc(message, False)[1].timestamp()))
        await state.set_state(None)
    except:
        txt = "When do you want me to remind you?\n\nError occured. Try writing the time like this:\nday month year time (for example 25 June 2024 15:35)"
        await user_data.get("message").edit_text(txt)
        await state.set_state(RNIForm.time)


@router.callback_query(F.data == "confirm_rni")
async def confirmed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    RNIManager().create_reminder(
        user_id=callback.from_user.id,
        purpose=user_data["purpose"],
        utc_timestamp=user_data["utc_timestamp"],
    )
    await state.clear()
    await callback.message.answer(text="Reminder created! ✅\nType /reminders to view all reminders.")


@router.callback_query(F.data == "refute_rni")
async def refuted(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Canceled.")
