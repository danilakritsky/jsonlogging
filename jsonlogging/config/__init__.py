import logging
import logging.handlers
from pathlib import Path

from .. import JSONFormatter

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
            "filename": "project.log",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "file"]},
}
