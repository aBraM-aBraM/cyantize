from src.consts import RESOURCE_DIR
from src.shared import CyantizeState
from src.file_type_scan import scan
import pytest


@pytest.fixture(scope="module")
def correct_files() -> set:
    return {file for file in RESOURCE_DIR.glob("*.correct.*") if file.is_file()}


@pytest.fixture(scope="module")
def incorrect_files():
    return {file for file in RESOURCE_DIR.glob("*.incorrect.*") if file.is_file()}


def test_filetype_sanity(config, correct_files, incorrect_files, mime_types):
    state = CyantizeState()
    state.add_files_to_scan(correct_files.union(incorrect_files))

    scan(config, state)

    assert len(state.files_passed) == len(correct_files), correct_files.difference(
        state.files_passed
    )
    assert len(state.files_failed) == len(incorrect_files), incorrect_files.difference(
        state.files_failed
    )


def test_filetype__where_file_without_extension():
    pass


def test_filetype__where_unsupported_extension():
    pass


def test_when_filetype_extension_fail_multiple_times_warning_issued(
    config, incorrect_files
):
    pass
