import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from database import ReminderManager
from handlers import common
from misc import get_utc_timestamp

router = Router()


async def remind(bot: Bot):
    for data in ReminderManager().get_all_reminders():
        if data[3] == get_utc_timestamp():
            await bot.send_message(data[1], text=f"{data[2]} reminder.")
            ReminderManager().delete_reminder(data[0])


async def run_bot():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    MY_TIMEZONE_AHEAD_SECONDS = os.getenv("MY_TIMEZONE_AHEAD_SECONDS")  # used in misc/funcs
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(remind, "interval", seconds=1, args=(bot,))
    scheduler.start()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="log.txt",
    )
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(common.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
