from loguru import logger


def setup():
    logger.info("Configuring base handlers ..")
    from . import start_command
