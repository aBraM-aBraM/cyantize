import toml
import pytest

from src.consts import MIME_TYPES_FILE, CONFIG_PATH
from src.config import CyantizeConfig


@pytest.fixture(scope="package")
def config() -> CyantizeConfig:
    config_dict = toml.load(CONFIG_PATH)
    config = CyantizeConfig.model_validate(config_dict)
    return config


@pytest.fixture(scope="package")
def mime_types():
    with open(MIME_TYPES_FILE) as f:
        return toml.load(f)
