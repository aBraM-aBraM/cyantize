import logging

import pytest

from cyantize.consts import MIME_TYPES_FILE
import cyantize
from cyantize.main import load_config
from cyantize.config import CyantizeConfig
from cyantize.file_type_scan import load_conflicts


@pytest.fixture(scope="package")
def config() -> CyantizeConfig:
    logging.disable(logging.CRITICAL)
    return load_config(cyantize.consts.CONFIG_TEMPLATE_FILE)


@pytest.fixture(scope="package")
def mime_types():
    return load_conflicts(MIME_TYPES_FILE)
