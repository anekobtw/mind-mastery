import time

from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import NotesManager
from keyboards import get_delete_keyboard, list_to_kb
from main import router

nm = NotesManager()


class NoteForm(StatesGroup):
    note = State()
    note_id = State()


@router.message(F.text, Command("take_note"))
async def take_note(message: types.Message, state: FSMContext) -> None:
    await state.set_state(NoteForm.note)
    await message.answer(text="Write a note. Type /cancel if you change your mind.")


@router.message(NoteForm.note)
async def process_note(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    nm.create_note(message.from_user.id, message.text)
    await message.answer(text="Note added! ✅\nType /notes to view all notes.")


@router.message(F.text, Command("notes"))
async def notes(message: types.Message) -> None:
    notes_list = nm.find_user_notes(message.from_user.id)
    if notes_list:
        notes = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(notes_list)])
        await message.answer(text=notes, reply_markup=list_to_kb(notes_list, "note"))
    else:
        await message.answer("You don't have any notes yet.\nType /take_note to create one.")


@router.callback_query(F.data.startswith("note_info_"))
async def note_info(callback: types.CallbackQuery):
    note = nm.get_note_info(note_id=callback.data.split("_")[2])

    text = (
        f"<b>Author's Telegram ID:</b> {note[1]}\n",
        f"<b>Text:</b> {note[2]}\n",
    )

    await callback.message.edit_text("".join(text), reply_markup=get_delete_keyboard(note[0], "note"))


@router.callback_query(F.data.startswith("delete_note_"))
async def delete_note(callback: types.CallbackQuery):
    action = callback.data.split("_")[2]

    if action != "cancel":
        nm.delete_note(int(action))
        await callback.message.edit_text(text="Deleted successfully! ✅")
        time.sleep(0.5)

    notes_list = nm.find_user_notes(callback.from_user.id)
    notes = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(notes_list)])
    if notes:
        await callback.message.edit_text(text=notes, reply_markup=list_to_kb(notes_list, "note"))
    else:
        await callback.message.edit_text(text="You don't have any notes yet.\nType /take_note to create one.")
