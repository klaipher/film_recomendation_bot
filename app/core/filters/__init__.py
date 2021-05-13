from aiogram import Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from loguru import logger


def setup(dispatcher: Dispatcher):
    logger.info("Configure filters...")
