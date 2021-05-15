from loguru import logger


def setup():
    logger.info("Configuring movies handlers ..")
    from . import rate_the_movie, random_recommendation, recommendation, selected_movie
