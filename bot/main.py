import asyncio
import logging
import os
import time

from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import get_handlers_router

start_time = time.time()


async def run_bot():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(get_handlers_router())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
