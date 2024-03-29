import os

from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import dotenv

from .handlers.default import register_handlers_default
from ..logger import logger

dotenv.load_dotenv()


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
    ]
    await bot.set_my_commands(commands)


async def start_bot():
    logger.info("Configuring...")
    
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_default(dp)

    await set_commands(bot)

    await dp.start_polling()
