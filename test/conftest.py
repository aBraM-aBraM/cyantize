import logging

import toml
import pytest

from cyantize.consts import MIME_TYPES_FILE, CONFIG_PATH
from cyantize.config import CyantizeConfig
from cyantize.file_type_scan import load_conflicts


@pytest.fixture(scope="package")
def config() -> CyantizeConfig:
    logging.disable(logging.CRITICAL)

    config_dict = toml.load(CONFIG_PATH)
    config = CyantizeConfig.model_validate(config_dict)
    return config


@pytest.fixture(scope="package")
def mime_types():
    return load_conflicts(MIME_TYPES_FILE)
