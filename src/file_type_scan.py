from pathlib import Path
import json
import logging
from magic import Magic
import mimetypes

from src.config import CyantizeConfig
from src.log import get_logger
from src.shared import CyantizeState, FAIL_EXTENSION_WARNING_COUNT
from src.consts import PROJECT_DIR

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


def get_mime_from_extension(
    file_path: Path, extension_to_mime: dict[str, str]
) -> str | None:
    extension = file_path.suffix[1:]
    if mimetype := mimetypes.guess_type(file_path)[0]:
        return mimetype
    if mimetype := extension_to_mime.get(extension):
        return mimetype
    return None


def scan(config: CyantizeConfig, state: CyantizeState) -> None:
    logger.info("starting filetype scan")

    with open(PROJECT_DIR / "apache-mime.types.txt") as mimes_file:
        extension_to_mime = json.load(mimes_file)

    magic = Magic(mime=True)

    for file_path in state.files_to_process:
        mime_from_extension = get_mime_from_extension(file_path, extension_to_mime)

        if not mime_from_extension:
            logging.warning("unknown extension", extra=dict(extension=file_path.suffix))
            continue

        with open(file_path, "rb") as file:
            mime_from_content = magic.from_buffer(file.read(1024))

        if file_path not in state.files_passed.keys():
            state.files_passed[str(file_path)] = True

        if mime_from_extension != mime_from_content:
            state.files_passed[str(file_path)] = False
            increase_extension_fail_count(state, file_path.suffix)
            logging.info(
                "file verification failed for %s extension",
                file_path,
                extra=dict(
                    mime_from_extension=mime_from_extension,
                    mime_from_content=mime_from_content,
                ),
            )
