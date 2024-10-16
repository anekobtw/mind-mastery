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


def wiki_buttons(results: list[str]) -> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text=f"{result}", callback_data=f"wiki_{result}")] for result in results]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def quotes_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Motivational", callback_data="quote_motivational")],
        [types.InlineKeyboardButton(text="Friendship", callback_data="quote_friendship")],
        [types.InlineKeyboardButton(text="Technology", callback_data="quote_technology")],
        [types.InlineKeyboardButton(text="Inspirational", callback_data="quote_inspirational")],
        [types.InlineKeyboardButton(text="Funny", callback_data="quote_funny")],
        [types.InlineKeyboardButton(text="Nature", callback_data="quote_nature")],
        [types.InlineKeyboardButton(text="Attitude", callback_data="quote_attitude")],
        [types.InlineKeyboardButton(text="Coding", callback_data="quote_coding")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def charts_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Bar chart", callback_data="chart_bar")],
        [types.InlineKeyboardButton(text="Line graph", callback_data="chart_line")],
        [types.InlineKeyboardButton(text="Pie chart", callback_data="chart_pie")],
        [types.InlineKeyboardButton(text="Doughnut chart", callback_data="chart_doughnut")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
