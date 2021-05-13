from loguru import logger


def setup():
    logger.info("Configuring errors handlers..")
    from . import errors
