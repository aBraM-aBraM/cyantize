import filetype
import magic

from src.config import CyantizeConfig
from src.log import get_logger
from src.shared import CyantizeState, FAIL_EXTENSION_WARNING_COUNT

logger = get_logger(__name__)


def increase_extension_fail_count(state: CyantizeState, extension: str) -> None:
    if extension in state.failed_extensions.keys():
        state.failed_extensions[extension] += 1
    else:
        state.failed_extensions[extension] = 1

    fail_count = state.failed_extensions[extension]
    if fail_count > FAIL_EXTENSION_WARNING_COUNT:
        logger.warning(
            "extension %s failed more than %d times. "
            "You can disable it manually by adding it to %s in the configuration",
            extension,
            fail_count,
            "filetypes.disabled_types",
        )


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
            increase_extension_fail_count(state, file_path.suffix)
            logger.info(
                "mismatch file extension to content %s",
                file_path,
                extra=dict(
                    file_type_from_content=file_type_from_content,
                    file_type_from_extension=file_type_from_extension,
                ),
            )
