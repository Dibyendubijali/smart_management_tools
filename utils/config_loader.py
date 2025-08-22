# utils/config_loader.py

import json
import logging
from pathlib import Path

logger = logging.getLogger("config_loader")

class ConfigLoader:
    """
    Helper class to load and save JSON-based config files.
    Used for server storage, app preferences, etc.
    """

    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            logger.info("Config file not found. Creating new one at %s", self.filepath)
            self.filepath.write_text(json.dumps({}, indent=2), encoding="utf-8")

    def load(self) -> dict:
        """Load JSON config file into dictionary."""
        try:
            with self.filepath.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON config (%s): %s", self.filepath, e)
            return {}
        except Exception as e:
            logger.exception("Unexpected error loading config %s: %s", self.filepath, e)
            return {}

    def save(self, data: dict) -> None:
        """Save dictionary to JSON config file."""
        try:
            with self.filepath.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Config saved successfully to %s", self.filepath)
        except Exception as e:
            logger.exception("Failed to save config %s: %s", self.filepath, e)
