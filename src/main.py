import click.types
import toml
from config import CyantizeConfig
from pathlib import Path


@click.command()
@click.argument("config_path", type=click.types.Path(exists=True, dir_okay=False))
@click.argument("scan_dir", type=click.types.Path(exists=True, file_okay=False))
def main(config_path: Path, scan_dir: Path) -> None:
    config_dict = toml.load(config_path)

    config = CyantizeConfig.model_validate(config_dict)

    print(config)
    print(type(config_path), type(scan_dir))


if __name__ == "__main__":
    main()
