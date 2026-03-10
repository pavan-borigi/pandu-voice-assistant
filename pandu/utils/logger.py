import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name="Pandu", level=logging.INFO):
    """Initializes and returns a logger instance with console and file handlers."""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if the logger is requested multiple times
    if logger.handlers:
        return logger
        
    logger.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler
    log_file = LOG_DIR / "pandu.log"
    fh = logging.FileHandler(str(log_file), encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Global instance for general use
logger = setup_logger()
