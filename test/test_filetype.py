from cyantize.shared import CyantizeState
from cyantize.file_type_scan import scan
from test.consts import RESOURCE_DIR
import pytest


@pytest.fixture(scope="module")
def correct_files() -> set:
    return {file for file in RESOURCE_DIR.glob("*.correct.*") if file.is_file()}


@pytest.fixture(scope="module")
def incorrect_files():
    return {file for file in RESOURCE_DIR.glob("*.incorrect.*") if file.is_file()}


def test_filetype_sanity(config, correct_files, incorrect_files):
    state = CyantizeState()
    state.add_files_to_scan(correct_files.union(incorrect_files))

    scan(config, state)

    assert len(state.files_passed) == len(correct_files), [str(p) for p in correct_files.difference(state.files_passed)]
    assert len(state.files_failed) == len(incorrect_files), [str(p) for p in incorrect_files.difference(state.files_failed)]


@pytest.mark.skip
def test_filetype_benchmark(config, correct_files, benchmark):
    state = CyantizeState()

    def multiple_run(run_state):
        for _ in range(10):
            run_state._file_to_status = dict()
            run_state.add_files_to_scan(correct_files)
            scan(config, run_state)

    benchmark(multiple_run, state)
    assert len(state.files_passed) == len(correct_files)


def test_filetype__where_file_without_extension():
    pass


def test_filetype__with_unsupported_extension():
    pass


def test_when_filetype_extension_fail_multiple_times_warning_issued(config, incorrect_files):
    pass
