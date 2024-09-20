from pathlib import Path

CONFIG_NAME = "cyantize.toml"

CYANTIZE_DIR = Path.home() / ".config" / "cyantize"
CONFIG_PATH = CYANTIZE_DIR / CONFIG_NAME

SRC_DIR = Path(__file__).parent
MIME_TYPES_FILE = SRC_DIR / "mime.types.txt"
CONFIG_TEMPLATE_FILE = SRC_DIR / CONFIG_NAME
