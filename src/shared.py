from pathlib import Path
from pydantic import BaseModel


class CyantizeState(BaseModel):
    files_to_process: list[Path]
    files_passed: dict[Path, bool] = dict()
