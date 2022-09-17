import sys

from loguru import logger


def configure_logger(capture_exceptions: bool = False) -> None:
    logger.remove()
    level = "INFO"
    logger.add("logs/log_{time:YYYY-MM-DD}.log", rotation="12:00",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}", level="INFO", encoding="utf-8")
    logger.add(sys.stdout, colorize=True,
               format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {file}:{line} | "
                      "{message}",
               level=level)
    if capture_exceptions:
        logger.add("logs/error_log_{time:YYYY-MM-DD}.log", rotation="12:00",
                   format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}", level="ERROR",
                   encoding="utf-8")