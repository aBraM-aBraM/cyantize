from pathlib import Path
from magic import Magic
import mimetypes

from src.config import CyantizeConfig
from src.log import get_logger
from src.shared import CyantizeState, FAIL_EXTENSION_WARNING_COUNT
from src.consts import MIME_TYPES_FILE

logger = get_logger(__name__)


def increase_extension_fail_count(state: CyantizeState, extension: str) -> None:
    if extension in state.failed_extensions.keys():
        state.failed_extensions[extension] += 1
    else:
        state.failed_extensions[extension] = 1

    fail_count = state.failed_extensions[extension]
    if fail_count == FAIL_EXTENSION_WARNING_COUNT + 1:
        logger.warning(
            "extension %s failed more than %d times. "
            "You can disable it manually by adding it to %s in the configuration",
            extension,
            FAIL_EXTENSION_WARNING_COUNT,
            "config.filetypes.suppress_extensions",
        )


def solve_conflict(
    mime_from_extension: str, mime_from_content: str, conflicts: dict[str, list[str]]
):
    extension_groups: list[set] = []

    for mime in [mime_from_extension, mime_from_content]:
        if extensions := conflicts.get(mime):
            extension_groups.append(set(extensions))
        else:
            logger.error(
                "unknown mimetype to conflicts can't be solved",
                extra=dict(mimetype=mime),
            )
            return

    extensions_from_extension, extensions_from_content = extension_groups
    return extensions_from_extension.intersection(extensions_from_content)


def load_conflicts(file_path: Path):
    conflicts: dict[str, list[str]] = {}
    with open(MIME_TYPES_FILE) as mimes_file:
        content = [line for line in mimes_file.readlines() if not line.startswith("#")]
        for mimetype, *extensions in content:
            conflicts[mimetype] = extensions
    return conflicts


def scan(config: CyantizeConfig, state: CyantizeState) -> None:
    logger.info("starting filetype scan")

    conflicts = load_conflicts(MIME_TYPES_FILE)
    magic = Magic(mime=True)
    mimetypes.init([MIME_TYPES_FILE])

    for file_path in state.files_to_scan:
        if file_path.suffix[1:] in config.filetypes.suppress_extensions:
            continue

        mime_from_extension = mimetypes.guess_type(file_path)[0]

        if not mime_from_extension:
            logger.error(
                "failed getting mime from extension",
                extra=dict(file_path=str(file_path)),
            )
            continue

        with open(file_path, "rb") as file:
            mime_from_content = magic.from_buffer(file.read(1024))

        if not mime_from_content:
            logger.error(
                "failed getting mime from content", extra=dict(file_path=str(file_path))
            )

        if mime_from_extension != mime_from_content:
            if not solve_conflict(mime_from_extension, mime_from_content, conflicts):
                state.set_file_invalid(file_path)
                increase_extension_fail_count(state, file_path.suffix)
                logger.info(
                    "file verification failed",
                    extra=dict(
                        file_path=str(file_path),
                        mime_from_extension=mime_from_extension,
                        mime_from_content=mime_from_content,
                    ),
                )
