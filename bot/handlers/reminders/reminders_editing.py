import time

from aiogram import F, types
from aiogram.filters import Command

from database import RNIManager, RWIManager
from keyboards import days_of_week, get_delete_keyboard, list_to_kb
from main import router
from misc import utc_to_local


@router.message(F.text, Command("reminders"))
async def reminders(message: types.Message) -> None:
    list_of_rwi_reminders = RWIManager().get_user_reminders(message.from_user.id)
    list_of_rni_reminders = RNIManager().get_user_reminders(message.from_user.id)

    if list_of_rni_reminders:
        reminders = "<b>Reminders without intervals:</b>\n"
        reminders += "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(list_of_rni_reminders)])
        await message.answer(
            text=reminders,
            reply_markup=list_to_kb(list_of_rni_reminders, "reminder_rni"),
        )
    else:
        await message.answer(
            "You don't have any reminders without intervals yet.\nType /create_reminder to create one."
        )

    if list_of_rwi_reminders:
        reminders = "<b>Reminders with intervals:</b>\n"
        reminders += "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(list_of_rwi_reminders)])
        await message.answer(
            text=reminders,
            reply_markup=list_to_kb(list_of_rwi_reminders, "reminder_rwi"),
        )
    else:
        await message.answer("You don't have any reminders with intervals yet.\nType /create_reminder to create one.")


@router.callback_query(F.data.startswith("reminder_rni_info"))
async def reminder_rni_info(callback: types.CallbackQuery):
    reminder_data = RNIManager().get_reminder_info(callback.data.split("_")[3])
    local_time = utc_to_local(callback.from_user.id, False, timestamp=reminder_data[3])
    await callback.message.edit_text(
        f"<b>Purpose:</b> {reminder_data[2]}\n<b>Time:</b> {local_time.strftime('%Y-%m-%d %H:%M:%S')}",
        reply_markup=get_delete_keyboard(reminder_data[0], "reminder_rni"),
    )


@router.callback_query(F.data.startswith("reminder_rwi_info"))
async def reminder_rwi_info(callback: types.CallbackQuery):
    reminder_data = RWIManager().get_reminder_info(callback.data.split("_")[3])
    local_time = utc_to_local(
        callback.from_user.id,
        True,
        hour=reminder_data[3],
        minute=reminder_data[4],
    )
    days = ", ".join(day for ind, day in enumerate(days_of_week) if ind in map(int, reminder_data[5].split(",")))
    await callback.message.edit_text(
        f"<b>Purpose:</b> {reminder_data[2]}\n<b>Time:</b> {local_time.hour}:{str(local_time.minute).zfill(2)}\n<b>Days:</b> {days}",
        reply_markup=get_delete_keyboard(reminder_data[0], "reminder_rwi"),
    )


@router.callback_query(F.data.startswith("delete_reminder_"))
async def delete_reminder(callback: types.CallbackQuery):
    action = callback.data.split("_")[3]
    rwi_or_rni = callback.data.split("_")[2]

    if action != "cancel":
        if rwi_or_rni == "rwi":
            RWIManager().delete_reminder(int(action))
        else:
            RNIManager().delete_reminder(int(action))
        await callback.message.edit_text(text="Deleted successfully!")
    else:
        list_of_rwi_reminders = RWIManager().get_user_reminders(callback.from_user.id)
        list_of_rni_reminders = RNIManager().get_user_reminders(callback.from_user.id)

        if rwi_or_rni == "rwi":
            reminders = "<b>Reminders with intervals:</b>\n"
            reminders += "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(list_of_rwi_reminders)])
            await callback.message.edit_text(
                text=reminders,
                reply_markup=list_to_kb(list_of_rwi_reminders, "reminder_rwi"),
            )
        else:
            reminders = "<b>Reminders without intervals:</b>\n"
            reminders += "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(list_of_rni_reminders)])
            await callback.message.edit_text(
                text=reminders,
                reply_markup=list_to_kb(list_of_rni_reminders, "reminder_rni"),
            )
