from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from misc.texts import links_text, start_text

router = Router()


@router.message(F.text, Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Canceled.", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text, Command("start", "help"))
async def start_command_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(start_text)


@router.message(F.text, Command("links"))
async def links(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(links_text, link_preview_options=types.LinkPreviewOptions(is_disabled=True))
