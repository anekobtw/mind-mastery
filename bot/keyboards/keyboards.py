from aiogram import types


def example() -> types.ReplyKeyboardMarkup:
    buttons = [["Example 1", "Example 2"], ["Example 3", "Example 4"]]

    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=btn) for btn in row] for row in buttons],
        resize_keyboard=True,
        input_field_placeholder="Choose an action",
    )


def get_notes_keyboard(notes_list: list) -> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text=str(ind + 1), callback_data=f"note_info_{str(val[0])}") for ind, val in enumerate(notes_list)]]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_delete_keyboard(note: list) -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_note_{note[0]}")],
        [types.InlineKeyboardButton(text="🔙 Go back", callback_data="delete_note_cancel")],
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