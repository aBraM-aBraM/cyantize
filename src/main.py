from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))  # noqa
import click.types
import pydantic
import toml
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.shared import CyantizeState
from src.config import CyantizeConfig
from src.log import get_logger
from src import file_type_scan

PROJECT_DIR = Path(__file__).parent.parent
logger = get_logger(__name__)


@click.command()
@click.argument("scan_dir", type=click.types.Path(exists=True, file_okay=False))
def main(scan_dir: Path) -> None:
    logger.info("start")

    config_path = PROJECT_DIR / "cyantize.toml"
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

    scanners = [file_type_scan.scan]

    futures = []
    names = []

    for scan_func in scanners:
        futures.append(pool.submit(scan_func, config, state))
        names.append(scan_func.__name__)

    for i, future in enumerate(as_completed(futures)):
        try:
            future.result()
        except Exception:
            logger.exception("scan %s failed", names[i])

    pool.shutdown(wait=True)
    logger.info("finish", extra=dict(files_passed=state.files_passed))


if __name__ == "__main__":
    main()
