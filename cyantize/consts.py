from pathlib import Path

CONFIG_FILENAME = "cyantize.toml"
PRIVATE_KEY_FILENAME = "private-key.pem"
PUBLIC_KEY_FILENAME = "public-key.pem"
LICENSE_FILENAME = "cyantize-license"

CYANTIZE_DIR = Path.home() / ".config" / "cyantize"
CONFIG_PATH = CYANTIZE_DIR / CONFIG_FILENAME
PUBLIC_KEY_PATH = CYANTIZE_DIR / PUBLIC_KEY_FILENAME
LICENSE_PATH = CYANTIZE_DIR / LICENSE_FILENAME

SRC_DIR = Path(__file__).parent
MIME_TYPES_FILE = SRC_DIR / "mime.types.txt"
CONFIG_TEMPLATE_FILE = SRC_DIR / CONFIG_FILENAME
