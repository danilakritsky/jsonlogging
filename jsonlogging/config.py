import logging
import logging.handlers
import sys
from pathlib import Path

from .jsonformatter import JSONFormatter

BASIC_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "console": {"()": JSONFormatter},
        "file": {"()": lambda: JSONFormatter(indent=None)},
    },
    "handlers": {
        "console": {
            "()": logging.StreamHandler,
            "level": "DEBUG",
            "formatter": "console",
        },
        "file": {
            "()": logging.FileHandler,
            "level": "INFO",
            "formatter": "file",
            "filename": "jsonlogging.log",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "file"]},
}


def dictConfigFromFile(path: str):
    """Use a dict stored in a file as logging configuration."""
