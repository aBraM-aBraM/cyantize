from pydantic import BaseModel
from pathlib import Path
import toml
import logging
from magic import Magic
import mimetypes

from src.config import CyantizeConfig
from src.log import get_logger
from src.shared import CyantizeState, FAIL_EXTENSION_WARNING_COUNT
from src.consts import MIME_TYPES_FILE, MIME_CONFLICTS_FILE

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


class Conflict(BaseModel):
    instances: list[str]
    reason: str


def scan(config: CyantizeConfig, state: CyantizeState) -> None:
    logger.info("starting filetype scan")

    with open(MIME_TYPES_FILE) as mimes_file:
        extension_to_mime = toml.load(mimes_file)

    with open(MIME_CONFLICTS_FILE) as mime_conflicts_file:
        # This is my organized way of solving conflicts between libmagic and mimetypes
        mime_conflicts_raw = toml.load(mime_conflicts_file)
        mime_conflicts = {
            extension: Conflict.model_validate(conflict)
            for extension, conflict in mime_conflicts_raw["conflicts"].items()
        }

    magic = Magic(mime=True)
    mimetypes.init()

    for file_path in state.files_to_scan:
        mime_from_extension = get_mime_from_extension(file_path, extension_to_mime)
        extension = file_path.suffix[1:]

        if not mime_from_extension:
            logging.warning("unknown extension", extra=dict(extension=extension))
            continue

        with open(file_path, "rb") as file:
            mime_from_content = magic.from_buffer(file.read(1024))
        if mime_from_extension != mime_from_content:
            if extension in mime_conflicts.keys():
                conflict = mime_conflicts[extension]
                if (
                    mime_from_extension in conflict.instances
                    and mime_from_content in conflict.instances
                ):
                    continue

            state.set_file_invalid(file_path)
            increase_extension_fail_count(state, file_path.suffix)
            logging.info(
                "file verification failed for %s extension",
                file_path,
                extra=dict(
                    mime_from_extension=mime_from_extension,
                    mime_from_content=mime_from_content,
                ),
            )
