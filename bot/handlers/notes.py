from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import NotesManager
from handlers.common import router
from keyboards import get_delete_keyboard, get_notes_keyboard

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
    await message.answer(text="Note added! Type /notes to view all notes.")


@router.message(F.text, Command("notes"))
async def notes(message: types.Message) -> None:
    notes_list = nm.find_notes(message.from_user.id)
    if notes_list is None:
        await message.answer("You don't have any notes yet.")
    else:
        notes = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(notes_list)])
        await message.answer(text=notes, reply_markup=get_notes_keyboard(notes_list))


@router.callback_query(F.data.startswith("note_info_"))
async def note_info(callback: types.CallbackQuery):
    note = nm.get_note_info(note_id=callback.data.split("_")[2])

    text = (
        f"<b>ID in database:</b> {note[0]}\n",
        f"<b>Author Telegram ID:</b> {note[1]}\n",
        f"<b>Text:</b> {note[2]}\n",
    )

    await callback.message.edit_text("".join(text), reply_markup=get_delete_keyboard(note))


@router.callback_query(F.data.startswith("delete_note_"))
async def delete_note(callback: types.CallbackQuery):
    action = callback.data.split("_")[2]

    if action == "cancel":
        notes_list = nm.find_notes(callback.from_user.id)
        notes = "\n".join([f"<b>{ind+1}.</b> {note[2]}\n" for ind, note in enumerate(notes_list)])
        await callback.message.edit_text(text=notes, reply_markup=get_notes_keyboard(notes_list))
    else:
        nm.delete_note(int(action))
        await callback.message.edit_text(text="Deleted successfully!")
