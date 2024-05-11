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
