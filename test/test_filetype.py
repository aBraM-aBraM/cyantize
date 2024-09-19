from test.consts import RESOURCE_DIR
from src.shared import CyantizeState
from src.filetype import scan
import pytest


@pytest.fixture(scope="module")
def files_to_process():
    return [file for file in RESOURCE_DIR.glob("*.correct.*") if file.is_file()]


def test_filetype_sanity(config, files_to_process):
    state = CyantizeState(files_to_process=files_to_process)

    scan(config, state)

    assert len(state.files_passed) == len(files_to_process)

    # TODO: add checks for fail types
    # TODO: check fail counts


def test_when_filetype_extension_fail_multiple_times_warning_issued(
    config, files_to_process
):
    pass
