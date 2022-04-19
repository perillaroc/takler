import logging


def get_logger(name: str = None) -> logging.Logger:
    try:
        from loguru import logger
        return logger
    except ImportError:
        pass

    parent_logger = logging.getLogger("takler")

    if name is not None:
        if not name.startswith(parent_logger.name + "."):
            logger = parent_logger.getChild(name)
        else:
            logger = logging.getLogger(name)
    else:
        logger = parent_logger

    return logger
