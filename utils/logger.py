import logging
from pathlib import Path

LOG_FILE = Path("logs/app.log")
LOG_FILE.parent.mkdir(exist_ok=True)  # Ensure logs folder exists

def setup_logging():
    """Configure centralized logging for the whole app."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("paramiko").setLevel(logging.WARNING)  # reduce SSH noise
    logging.info("Logging initialized. Writing to %s", LOG_FILE)
