from pathlib import Path
from pydantic import BaseModel

FAIL_EXTENSION_WARNING_COUNT = 10


class CyantizeState(BaseModel):
    files_to_process: list[Path]
    files_passed: dict[Path, bool] = dict()
    failed_extensions: dict[str, int] = dict()
