from aiogram import types


def list_to_kb(ListToBeIterated: list[str], prefix: str) -> types.InlineKeyboardMarkup:
    buttons = []
    for i in range(0, len(ListToBeIterated), 8):
        row_buttons = [
            types.InlineKeyboardButton(text=str(ind + 1 + i), callback_data=f"{prefix}_info_{str(val[0])}")
            for ind, val in enumerate(ListToBeIterated[i : i + 8])
        ]
        buttons.append(row_buttons)
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_delete_keyboard(id: int, prefix: str) -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_{prefix}_{id}")],
        [types.InlineKeyboardButton(text="🔙 Go back", callback_data=f"delete_{prefix}_cancel")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_keyboard(suffix: str) -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="✅", callback_data=f"confirm_{suffix}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"refute_{suffix}"),
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def website_button(web_app_info: types.WebAppInfo) -> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text="Open the website", web_app=web_app_info)]]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_reminders_kb() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="With intervals", callback_data="with_intervals"),
            types.InlineKeyboardButton(text="Without intervals", callback_data="without_intervals"),
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]  # I imported it in reminder_with_intervals


def get_week_kb(selected_days: list[str]) -> types.InlineKeyboardMarkup:
    buttons = [[], [types.InlineKeyboardButton(text="Confirm", callback_data="confirm_week")]]

    for i, day in enumerate(days_of_week):
        buttons[0].append(types.InlineKeyboardButton(text=f"{day} ✅" if selected_days[i] else day, callback_data=f"week_{day}"))

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
