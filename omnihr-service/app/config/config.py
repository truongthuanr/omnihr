# config/config.py
import json
import os
import time
from pathlib import Path

from app.servicelog.servicelog import logger

# default config use incase user's config is missed.
DEFAULT_COLUMNS = {
    "id": False,
    "first_name": True,
    "last_name": True,
    "contact": True,
    "department": True,
    "position": True,
    "location": True,
    "company": True
}

class Config:
    def __init__(self, ttl: int = 60):
        # TODO: if file not found, use the default config file.
        path = os.getenv("CONFIG_PATH", "/app/config/config.json")
        self._path = Path(path)
        self._ttl = ttl
        self._last_load = 0
        self._cache = {}

    def _load(self):
        try:
            with self._path.open("r") as f:
                self._cache = json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {self._path}")
            raise RuntimeError("Config file missing — please provide a valid config.")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config: {e}")
            raise RuntimeError("Config file is not valid JSON.")

    def _load_if_needed(self):
        now = time.time()
        if now - self._last_load > self._ttl:
            logger.info(f"Loading configuration from file {self._path}")
            self._load()
        else:
            logger.info(f"Use cache configuration, no loading.")

    def get_enabled_columns(self) -> list[str]:
        logger.info(f"Getting configuration for output collumns.")
        self._load_if_needed()
        columns = self._cache.get("columns", {})
        merged = {**DEFAULT_COLUMNS, **columns}
        return [col for col, enabled in merged.items() if enabled]

config = Config()
