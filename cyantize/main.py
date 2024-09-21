from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))  # noqa
import click.types
import pydantic
import toml
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from cyantize.shared import CyantizeState
from cyantize.config import CyantizeConfig
from cyantize.log import get_logger
from cyantize.consts import CYANTIZE_DIR, CONFIG_TEMPLATE_FILE, CONFIG_PATH, PUBLIC_KEY_PATH, LICENSE_PATH
from cyantize import file_type_scan
from cyantize.license import SignedCyantizeLicense

logger = get_logger(__name__)


def load_config(config_path: Path) -> CyantizeConfig:
    try:
        config_dict = toml.load(config_path)
    except toml.TomlDecodeError:
        logger.exception("Failed loading toml config. Make sure %s is toml", CONFIG_PATH)
        raise
    except (IOError, FileNotFoundError):
        logger.exception("Failed loading config. %s doesn't exist", CONFIG_PATH)
        raise

    try:
        return CyantizeConfig.model_validate(config_dict)
    except pydantic.ValidationError:
        logger.exception("config value can't be validated")
        raise


def first_time_init():
    logger.info(
        "first installation creating cyantize dir",
        extra=dict(cyantize_dir=str(CYANTIZE_DIR)),
    )
    CYANTIZE_DIR.mkdir()
    logger.info("creating default config", extra=dict(config_path=CONFIG_PATH))
    shutil.copy(CONFIG_TEMPLATE_FILE, CONFIG_PATH)


@click.command()
@click.argument("scan_dir", type=click.types.Path(exists=True, file_okay=False))
def main(scan_dir: Path) -> None:
    logger.info("start")

    if not CYANTIZE_DIR.exists():
        first_time_init()

    cyantize_license = SignedCyantizeLicense.from_file(LICENSE_PATH, PUBLIC_KEY_PATH)
    logger.info("loaded license", extra=cyantize_license.model_dump())

    config = load_config(CONFIG_PATH)

    # This state is not thread-safe it is only written to here
    # before more threads appear. All other threads should only read from it
    state = CyantizeState()
    state.add_files_to_scan({file for file in Path(scan_dir).rglob("*") if file.is_file()})
    logger.info("processing files", extra=dict(file_count=len(state.files_to_scan)))

    futures = []
    names = []

    with ThreadPoolExecutor() as pool:
        for scan_func in [file_type_scan.scan]:
            futures.append(pool.submit(scan_func, config, state))
            names.append(scan_func.__name__)

        for i, future in enumerate(as_completed(futures)):
            try:
                future.result()
            except Exception:
                logger.exception("scan %s failed", names[i])

    logger.info("finish", extra=dict(files_passed=[str(f) for f in state.files_passed]))
