import logging
import os
import sys
from pythonjsonlogger import jsonlogger


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s"  # noqa
    )

    file_handler = logging.FileHandler("cyantize.log")
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler(sys.stderr)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    logger.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO")))

    return logger
