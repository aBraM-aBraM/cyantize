import click.types
import toml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import shared
from config import CyantizeConfig
import filetype


@click.command()
@click.argument("config_path", type=click.types.Path(exists=True, dir_okay=False))
@click.argument("scan_dir", type=click.types.Path(exists=True, file_okay=False))
def main(config_path: Path, scan_dir: Path) -> None:
    config_dict = toml.load(config_path)

    config = CyantizeConfig.model_validate(config_dict)

    files_to_process = [file for file in Path(scan_dir).rglob("*") if file.is_file()]
    shared.g_state.processed_file_count = len(files_to_process)

    pool = ThreadPoolExecutor()

    scanners = [(filetype.scan, config.filetypes)]

    for scan_func, scan_conf in scanners:
        pool.submit(scan_func, scan_conf, files_to_process)


if __name__ == "__main__":
    main()
