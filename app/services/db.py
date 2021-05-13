from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from loguru import logger
from tortoise import Tortoise, exceptions

from app import config
from app.models import MODELS


async def on_startup(_dp: Dispatcher):
    try:
        await Tortoise.init(
            db_url=config.SQLITE_URI,
            modules={"models": MODELS},
        )
        await Tortoise.generate_schemas()
        logger.info("SQLite Connection opened")
    except (exceptions.ConfigurationError, ConnectionError) as e:
        logger.error(f"Database initialization error: {e}")


async def on_shutdown(_dp: Dispatcher):
    await Tortoise.close_connections()  # it will raise logging info


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
