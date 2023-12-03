import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot, Router, types
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from dotenv import load_dotenv

from database import database as db

from routers import router as all_routers

load_dotenv('.env')

router = Router()
router.include_router(all_routers)


async def on_startup():
    await db.db_start()
    print("Baza ishga tushdi!")


async def on_shutdown():
    await db.close()
    print("Baza to'xtatildi!")


async def main() -> None:
    dp = Dispatcher()

    dp.include_router(router)
    bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    commands = [
        BotCommand(command='start', description='Botni ishga tushurish ♻')
    ]
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped!')
