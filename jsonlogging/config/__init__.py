from pathlib import Path
import logging
import logging.handlers
from .. import JSONFormatter

BASIC_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
      "console": {
        "()": JSONFormatter
      },
      "file": {
        "()": lambda: JSONFormatter(indent=None)
      }
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
        "filename": "logname.log",
      },
    },

    "root": {
      "level": "INFO",
      "handlers": ["console", "file"]
    }
}


def dictConfigFromFile(
    path: str | Path,
    filename: str = 'jsondictconfig.py') -> None:
    """Create a file containing a dictionary with basic logging config."""
    path = Path(str) if isinstance(path, str) else path
    fullpath = path / filename
    if not fullpath.exists():
        path.mkdir(parents=True, exist_ok=True)
        with open(path / filename, 'w') as f:
            f.write(str(BASIC_CONFIG))
    # else:
    #     with open(fullpath, 'r') as f:
    #         res = f.read()
    #     return res
