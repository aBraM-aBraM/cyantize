from test.consts import FILETYPE_CORRECT_DIR
from src.shared import CyantizeState
from src.filetype import scan
import pytest


@pytest.fixture(scope="module")
def files_to_process():
    return [file for file in FILETYPE_CORRECT_DIR.glob("*") if file.is_file()]


def test_filetype_sanity(config, files_to_process):
    state = CyantizeState(files_to_process=files_to_process)

    scan(config, state)

    assert len(state.files_passed) == len(files_to_process)
