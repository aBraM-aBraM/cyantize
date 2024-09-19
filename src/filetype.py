from src.config import CyantizeConfig
from src.log import get_logger
from src.shared import CyantizeState

logger = get_logger(__name__)


def scan(config: CyantizeConfig, state: CyantizeState) -> None:
    logger.info("starting filetype scan")
    logger.debug("supported file types: %s", config.filetypes.filetypes)
    for file in state.files_to_process:
        logger.info("scanning %s", file)
