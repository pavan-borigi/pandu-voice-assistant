import yaml
from pathlib import Path
from utils.logger import logger

CONFIG_FILE = Path(__file__).parent.parent / "config.yaml"

def load_config() -> dict[str, any]:
    """Loads configuration from the config.yaml file."""
    if not CONFIG_FILE.exists():
        logger.warning(f"Configuration file not found at {CONFIG_FILE}. Using defaults.")
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config is None:
                return {}
            return config
    except Exception as e:
        logger.error(f"Failed to load config file: {e}")
        return {}

# Load it once globally
config = load_config()
