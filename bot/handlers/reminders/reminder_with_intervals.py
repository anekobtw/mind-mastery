from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import RWIManager
from keyboards import days_of_week, get_week_kb
from main import router
from misc import local_to_utc


class RWIForm(StatesGroup):
    purpose = State()
    time = State()


@router.callback_query(F.data == "with_intervals")
async def with_intervals(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Okay, let's create one with intervals. Remember that you can type /cancel at any time if you change your mind."
    )
    msg = await callback.message.answer("What do you want me to remind you of?")
    await state.update_data(selected_days=[False, False, False, False, False, False, False])
    await state.update_data(message=msg)
    await state.set_state(RWIForm.purpose)


@router.message(RWIForm.purpose)
async def process_purpose(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if not user_data.get("purpose"):
        await state.update_data(purpose=message.text)
    await user_data["message"].edit_text(
        "Please, select the days on which I'll remind you, then press confirm",
        reply_markup=get_week_kb(user_data["selected_days"]),
    )


@router.callback_query(F.data.startswith("week_"))
async def process_weeks(callback: types.CallbackQuery, state: FSMContext):
    callback_day = callback.data.split("_")[1]
    index = days_of_week.index(callback_day)

    user_data = await state.get_data()
    user_data["selected_days"][index] = not user_data["selected_days"][index]
    await process_purpose(callback.message, state)


@router.callback_query(F.data.startswith("confirm_week"))
async def confirm_week(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    selected_days = user_data["selected_days"]

    if any(selected_days):
        await user_data["message"].edit_text(
            "Please, write the time as HOURS:MINUTES (for example, 13:55)"
        )
        await state.set_state(RWIForm.time)
    else:
        await callback.answer("Error occured. Please, choose at least one day.")


@router.message(RWIForm.time)
async def process_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        RWIManager().create_reminder(
            user_id=message.from_user.id,
            purpose=user_data["purpose"],
            hour=local_to_utc(message, True)[0],
            minute=local_to_utc(message, True)[1],
            days=",".join(
                [
                    str(ind)
                    for ind, day in enumerate(days_of_week)
                    if user_data["selected_days"][ind]
                ]
            ),
        )
        await user_data["message"].edit_text("Created!")
        await state.clear()
    except:
        await message.answer(
            "Error occured. Please, try again. Write the time as HOURS:MINUTES (for example, 13:55)"
        )
        await state.set_state(RWIForm.time)
