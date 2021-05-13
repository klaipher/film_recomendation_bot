from loguru import logger


def setup():
    logger.info("Configure handlers...")
    from . import base, errors

    errors.setup()
    base.setup()
