from aiogram import Dispatcher
from loguru import logger


def setup(dispatcher: Dispatcher):
    logger.info("Configure middlewares...")
    from aiogram.contrib.middlewares.logging import LoggingMiddleware

    from app.core.middlewares.acl import ACLMiddleware
    from app.core.middlewares.trottling import ThrottlingMiddleware\

    dispatcher.middleware.setup(LoggingMiddleware("bot"))
    dispatcher.middleware.setup(ThrottlingMiddleware())
    dispatcher.middleware.setup(ACLMiddleware())
