from pathlib import Path
from pydantic import BaseModel

FAIL_EXTENSION_WARNING_COUNT = 10


class CyantizeState(BaseModel):
    # using this data structure to allow scanners to |=
    # the value of the current status and prune making this
    # thread safe
    _file_to_status: dict[str, bool] = dict()
    failed_extensions: dict[str, int] = dict()

    def add_files_to_scan(self, files: list[Path]):
        for file in files:
            self._file_to_status[str(file)] = True

    def set_file_invalid(self, file: Path):
        self._file_to_status[str(file)] = False

    @property
    def files_to_scan(self):
        return [Path(file) for file, has_passed in self._file_to_status.items()]

    @property
    def files_passed(self):
        return [
            Path(file)
            for file, has_passed in self._file_to_status.items()
            if has_passed
        ]

    @property
    def files_failed(self):
        return [
            Path(file)
            for file, has_passed in self._file_to_status.items()
            if not has_passed
        ]
