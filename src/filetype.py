from pathlib import Path
from config import FileTypeConfig
from log import get_logger

logger = get_logger(__name__)


def scan(config: FileTypeConfig, files_to_process: list[Path]) -> None:
    logger.info("starting filetype scan")
    logger.debug("supported file types: %s", config.filetypes)
    for file in files_to_process:
        logger.info("scanning %s", file)
