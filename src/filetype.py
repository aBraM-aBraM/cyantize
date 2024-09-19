from pathlib import Path
from config import FileTypeConfig


def scan(config: FileTypeConfig, files_to_process: list[Path]) -> None:
    print(f"got config {config}")
    for file in files_to_process:
        print(f"scanning {file}")
