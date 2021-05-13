from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from loguru import logger

from app.misc import dp


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(_update, _error):
    return True


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
    return True
