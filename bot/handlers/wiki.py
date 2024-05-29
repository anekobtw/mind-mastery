import wikipedia
from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import website_button, wiki_buttons
from main import router


class WikiForm(StatesGroup):
    page = State()


@router.message(F.text, Command("wikipedia"))
async def wikipedia_command(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(WikiForm.page)
    await message.answer(
        "What do you want to search for?\nType /cancel if you don't want to search anymore."
    )


@router.message(WikiForm.page)
async def process_page(message: types.Message, state: FSMContext):
    results = wikipedia.search(message.text, results=5)
    if results:
        await message.answer(
            text="<b>Choose an article</b>\n\n"
            + "\n".join([f"<b>{ind+1}.</b> {result}\n" for ind, result in enumerate(results)]),
            reply_markup=wiki_buttons(message.text, 5),
        )
    else:
        await message.answer("No results found.")

    await state.clear()


@router.callback_query(F.data.startswith("wiki_"))
async def wiki_info(callback: types.CallbackQuery):
    _, query, ind = callback.data.split("_")
    results = wikipedia.search(query, results=5)

    try:
        page = wikipedia.page(results[int(ind) - 1], auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        page = wikipedia.page(e.options[0])

    await callback.message.answer(
        f"<b>{page.original_title}</b>\n\n{page.summary[:1000]}...",
        reply_markup=website_button("Open full article", types.WebAppInfo(url=page.url)),
    )
