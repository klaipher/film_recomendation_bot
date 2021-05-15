from loguru import logger


def setup():
    logger.info("Configure handlers...")
    from . import base, errors, movies

    errors.setup()
    base.setup()
    movies.setup()
