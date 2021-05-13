from aiogram.utils.executor import Executor
from loguru import logger

from app.services import apscheduller, db, parser


def setup(runner: Executor):
    logger.info("Configure services...")
    db.setup(runner)
    apscheduller.setup(runner)
    parser.setup(runner)
