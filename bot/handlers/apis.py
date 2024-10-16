import json

import requests
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import charts_keyboard

router = Router()


class ChartForm(StatesGroup):
    labels = State()
    items = State()


@router.message(F.text, Command("dog"))
async def dog(message: types.Message, state: FSMContext):
    await state.clear()
    result = requests.get("https://dog.ceo/api/breeds/image/random")
    if result.status_code == 200:
        await message.answer_photo(photo=types.URLInputFile(result.json()["message"]))


@router.message(F.text, Command("fox"))
async def dog(message: types.Message, state: FSMContext):
    await state.clear()
    result = requests.get("https://randomfox.ca/floof/")
    if result.status_code == 200:
        await message.answer_photo(photo=types.URLInputFile(result.json()["image"]))


@router.message(F.text, Command("joke"))
async def dadjoke(message: types.Message, state: FSMContext):
    await state.clear()

    result = requests.get("https://official-joke-api.appspot.com/random_joke")
    setup = result.json().get("setup")
    punchline = result.json().get("punchline")
    if result.status_code == 200:
        await message.answer(f"{setup}\n<span class='tg-spoiler'>{punchline}</span>")


@router.message(F.text, Command("chart"))
async def chart(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose an option", reply_markup=charts_keyboard())


@router.callback_query(F.data.startswith("chart_"))
async def process_chart(callback: types.CallbackQuery, state: FSMContext):
    _, type = callback.data.split("_")

    post_data = {"chart": {"type": type, "data": {"labels": ["Label1", "Label2"], "datasets": [{"label": "Item1", "data": [1, 2]}, {"label": "Item2", "data": [3, 4]}]}}}
    response = requests.post("https://quickchart.io/chart/create", json=post_data)

    await state.update_data(chart_type=type)
    await callback.message.answer_photo(photo=types.URLInputFile(json.loads(response.text)["url"]), caption="Here's the example.\nNow send me all the labels separated by a comma (e.g. Label1, Label2).")
    await callback.message.delete()
    await state.set_state(ChartForm.labels)


@router.message(ChartForm.labels)
async def process_labels(message: types.Message, state: FSMContext):
    await state.update_data(labels=message.text.split(","))
    await message.answer("Now send me the items separated by a semicolon, values assigned to them separated by a dash, and values separated by a comma. (e.g. Item1 - 1, 2; Item2 - 3, 4)")
    await state.set_state(ChartForm.items)


@router.message(ChartForm.items)
async def send_chart(message: types.Message, state: FSMContext):
    data = await state.get_data()
    labels = data.get("labels")
    chart_type = data.get("chart_type")  # Retrieve the chart type stored earlier
    datasets = message.text.split(";")  # Split datasets

    formatted_datasets = []
    for dataset in datasets:
        label, values = dataset.split("-")
        values = list(map(int, values.split(",")))  # Convert string values to int
        formatted_datasets.append({"label": label.strip(), "data": values})

    post_data = {"chart": {"type": chart_type, "data": {"labels": labels, "datasets": formatted_datasets}}}  # Use the chart type stored in FSM

    response = requests.post("https://quickchart.io/chart/create", json=post_data)

    await message.answer_photo(photo=types.URLInputFile(json.loads(response.text)["url"]))
    await state.clear()
