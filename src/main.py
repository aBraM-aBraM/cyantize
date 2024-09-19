import click.types
import pydantic
import toml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import shared
from config import CyantizeConfig
from log import get_logger
import filetype

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
    shared.g_state.processed_file_count = len(files_to_process)
    logger.info("processing %d files", shared.g_state.processed_file_count)

    pool = ThreadPoolExecutor()

    scanners = [(filetype.scan, config.filetypes)]

    for scan_func, scan_conf in scanners:
        pool.submit(scan_func, scan_conf, files_to_process)


if __name__ == "__main__":
    main()
