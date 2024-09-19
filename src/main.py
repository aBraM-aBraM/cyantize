import click.types
import toml
from config import CyantizeConfig


@click.command()
@click.argument("config_path", type=click.types.Path(exists=True, dir_okay=False))
def main(config_path):
    config_dict = toml.load(config_path)

    config = CyantizeConfig.model_validate(config_dict)

    print(config_dict, config)


if __name__ == '__main__':
    main()
