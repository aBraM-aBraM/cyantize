from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
TEST_DIR = PROJECT_DIR / "test"
RESOURCE_DIR = TEST_DIR / "resource"

FILETYPE_CORRECT_DIR = RESOURCE_DIR / "filetype_correct"
FILETYPE_INCORRECT_DIR = RESOURCE_DIR / "filetype_incorrect"
