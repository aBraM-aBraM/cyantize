from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_DIR / "cyantize.toml"
TEST_DIR = PROJECT_DIR / "test"
RESOURCE_DIR = TEST_DIR / "resource"

MIME_TYPES_FILE = PROJECT_DIR / "mime.types.txt"
