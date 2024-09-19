from src.consts import RESOURCE_DIR
from src.shared import CyantizeState
from src.file_type_scan import scan
import pytest


@pytest.fixture(scope="module")
def correct_files():
    return [file for file in RESOURCE_DIR.glob("*.correct.*") if file.is_file()]


@pytest.fixture(scope="module")
def incorrect_files():
    return [file for file in RESOURCE_DIR.glob("*.incorrect.*") if file.is_file()]


def test_filetype_sanity(config, correct_files, incorrect_files):
    state = CyantizeState(files_to_process=correct_files + incorrect_files)

    scan(config, state)

    files_pass_count = sum(state.files_passed.values())
    files_fail_count = len(state.files_to_process) - files_pass_count
    assert files_pass_count == len(correct_files)
    assert files_fail_count == len(incorrect_files)


def test_when_filetype_extension_fail_multiple_times_warning_issued(
    config, incorrect_files
):
    pass
