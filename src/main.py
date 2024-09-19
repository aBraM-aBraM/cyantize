from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))  # noqa
import click.types
import pydantic
import toml
from concurrent.futures import ThreadPoolExecutor

from src.shared import CyantizeState
from src.config import CyantizeConfig
from src.log import get_logger
from src import filetype

logger = get_logger(__name__)


@click.command()
@click.argument("config_path", type=click.types.Path(exists=True, dir_okay=False))
@click.argument("scan_dir", type=click.types.Path(exists=True, file_okay=False))
def main(config_path: Path, scan_dir: Path) -> None:
    logger.info("start")
    try:
        config_dict = toml.load(config_path)
    except toml.TomlDecodeError:
        logger.exception(
            "Failed loading toml config. Make sure %s is toml", config_path
        )
        raise
    except (IOError, FileNotFoundError):
        logger.exception("Failed loading config. %s doesn't exist", config_path)
        raise

    try:
        config = CyantizeConfig.model_validate(config_dict)
    except pydantic.ValidationError:
        logger.exception("config value can't be validated")
        raise

    files_to_process = [file for file in Path(scan_dir).rglob("*") if file.is_file()]

    # This state is not thread-safe it is only written to here
    # before more threads appear. All other threads should only read from it
    state = CyantizeState(files_to_process=files_to_process)
    logger.info("processing %d files", len(state.files_to_process))

    pool = ThreadPoolExecutor()

    scanners = [filetype.scan]

    for scan_func in scanners:
        pool.submit(scan_func, config, state)


if __name__ == "__main__":
    main()
