import logging.config
from .jsonformatter import JSONFormatter

from .config import BASIC_CONFIG


def basicConfig():
    """Configure basic JSON logging."""
    logging.config.dictConfig(BASIC_CONFIG)
