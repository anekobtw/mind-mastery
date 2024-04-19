from aiogram import types


def get_nums_kb(some_list: list[str], what: str) -> types.InlineKeyboardMarkup:
    buttons = []
    for i in range(0, len(some_list), 8):
        row_buttons = [
            types.InlineKeyboardButton(text=str(ind + 1 + i), callback_data=f"{what}_info_{str(val[0])}")
            for ind, val in enumerate(some_list[i : i + 8])
        ]
        buttons.append(row_buttons)
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_delete_keyboard(what1: list, what2: str) -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_{what2}_{what1[0]}")],
        [types.InlineKeyboardButton(text="🔙 Go back", callback_data=f"delete_{what2}_cancel")],
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
