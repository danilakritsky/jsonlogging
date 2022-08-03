import logging.config

from .config import BASIC_CONFIG
from .jsonformatter import LOGRECORD_ATTRS, JSONFormatter


def basicConfig():
    """Configure basic JSON logging."""
    logging.config.dictConfig(BASIC_CONFIG)
