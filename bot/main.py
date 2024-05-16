import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from database import RNIManager, RWIManager
from handlers import common
from misc import get_utc_timestamp

router = Router()


async def remind_rni(bot: Bot) -> None:
    # without intervals
    for data in RNIManager().get_all_reminders():
        if data[3] <= get_utc_timestamp():
            await bot.send_message(
                data[1],
                text=f"❗ Hey, just reminding you about <b>{data[2]}</b>.",
                disable_notification=False,
            )
            RNIManager().delete_reminder(data[0])


async def remind_rwi(bot: Bot) -> None:
    # with intervals
    for data in RWIManager().get_all_reminders():
        dt = datetime.fromtimestamp(get_utc_timestamp())
        if dt.hour == data[3] and dt.minute == data[4] and datetime.today().weekday() in map(int, data[5].split(",")):
            await bot.send_message(
                data[1],
                text=f"❗ Hey, just reminding you about <b>{data[2]}</b>.",
                disable_notification=False,
            )


async def run_bot():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(remind_rni, "interval", seconds=1, args=(bot,))
    scheduler.add_job(remind_rwi, "interval", seconds=60, args=(bot,))
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
