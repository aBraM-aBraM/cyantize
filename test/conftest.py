import toml
import pytest

from test.consts import PROJECT_DIR
from src.config import CyantizeConfig


@pytest.fixture(scope="package")
def config() -> CyantizeConfig:
    config_dict = toml.load(PROJECT_DIR / "cyantize.toml")
    config = CyantizeConfig.model_validate(config_dict)
    return config
