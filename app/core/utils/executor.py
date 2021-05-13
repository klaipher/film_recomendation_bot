from aiogram.utils.executor import Executor
from loguru import logger

from app import services
from app.misc import dp

runner = Executor(dp)


def setup():
    services.setup(runner)
    logger.info("Configure executor...")
