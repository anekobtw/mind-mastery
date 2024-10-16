import wikipedia
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import wiki_buttons

router = Router()


class WikiForm(StatesGroup):
    page = State()


@router.message(F.text, Command("wikipedia"))
async def wikipedia_command(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(WikiForm.page)
    await message.answer("What do you want to search for?\nType /cancel if you don't want to search anymore.")


@router.message(WikiForm.page)
async def process_page(message: types.Message, state: FSMContext):
    results = wikipedia.search(message.text, results=10)
    if results:
        await message.answer(text="<b>Choose an article</b>", reply_markup=wiki_buttons(results))
    else:
        await message.answer("No results found.")
    await state.clear()


@router.callback_query(F.data.startswith("wiki_"))
async def wiki_info(callback: types.CallbackQuery):
    _, query = callback.data.split("_")

    page = wikipedia.page(query, auto_suggest=False)
    await callback.message.edit_text(text=f"<b>{page.original_title}</b>\n\n{page.summary[:1000]}...", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Read full article", callback_data=f"wikifull_{query}")]]))


@router.callback_query(F.data.startswith("wikifull_"))
async def read_full(callback: types.CallbackQuery):
    _, query = callback.data.split("_")

    page = wikipedia.page(query, auto_suggest=False)
    for section in page.sections:
        if page.section(section):
            await callback.message.answer(f"<b>{section}</b>\n{page.section(section)[:1900]}")
