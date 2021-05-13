import asyncio
import concurrent.futures

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app import config

loop = asyncio.get_event_loop()

bot = Bot(config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
bot_username = loop.run_until_complete(bot.me).username
storage = MemoryStorage()

asyncio_executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

dp = Dispatcher(bot, storage=storage, loop=loop)


def setup():
    from app import handlers
    from app.core import filters, middlewares
    from app.core.utils import executor

    middlewares.setup(dp)
    filters.setup(dp)
    executor.setup()

    handlers.setup()
