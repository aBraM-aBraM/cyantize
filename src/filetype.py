import filetype
import magic

from src.config import CyantizeConfig
from src.log import get_logger
from src.shared import CyantizeState

logger = get_logger(__name__)


def scan(config: CyantizeConfig, state: CyantizeState) -> None:
    logger.info("starting filetype scan")

    mime = magic.Magic(mime=True)

    for file_path in state.files_to_process:
        file_type_from_extension = filetype.guess(file_path).mime

        with file_path.open("rb") as file:
            file_type_from_content = mime.from_buffer(file.read(1024))

        if file_path not in state.files_passed.keys():
            state.files_passed[file_path] = True

        if file_type_from_extension != file_type_from_content:
            state.files_passed[file_path] = False
            logger.info(
                "mismatch file extension to content %s",
                file_path,
                extra=dict(
                    file_type_from_content=file_type_from_content,
                    file_type_from_extension=file_type_from_extension,
                ),
            )
