from aiogram import types


def list_to_kb(ListToBeIterated: list[str], prefix: str) -> types.InlineKeyboardMarkup:
    buttons = []
    for i in range(0, len(ListToBeIterated), 8):
        row_buttons = [
            types.InlineKeyboardButton(
                text=str(ind + 1 + i),
                callback_data=f"{prefix}_info_{str(val[0])}",
            )
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


def website_button(text: str, web_app_info: types.WebAppInfo) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=text, web_app=web_app_info)]])


def get_reminders_kb() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="With intervals", callback_data="with_intervals"),
            types.InlineKeyboardButton(text="Without intervals", callback_data="without_intervals"),
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def wiki_buttons(search_query: str, length: int) -> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text=f"{i+1}", callback_data=f"wiki_{search_query}_{i+1}") for i in range(length)]]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
