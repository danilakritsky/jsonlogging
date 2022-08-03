import copy
import datetime
import json
import logging
import logging.config
import typing
from pathlib import Path
from typing import Any, Callable, Iterable



# https://betterprogramming.pub/4-new-type-annotation-features-in-python-3-11-84e7ec277c29

# https://docs.python.org/3/library/logging.html#logrecord-attributes
LOGRECORD_ATTRS: tuple[str, ...] = (
    "args",
    "asctime",
    "created",
    "exc_info",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
)


class JSONFormatter:
    """Log formatter object that formats records as JSON strings
    with braces-tyle string interpolation support.

    See examples for usage info.

    parameters
    ----------
        fields: Iterable[str] | str | None = None
            LogRecord's attributes that should be logged.
            If None - log all fields.
        datefmt: str = '%Y-%m-%d %H:%M:%S'
            Date format for asctime field.
        indent: int = 2
            JSON indendation level.

    returns
    -------
        JSONFormatter

    raises
    ------
        TypeError
            If invalid type is passed as an argument to fields.

    examples
    --------
    Selecting fields to log:

    >>> import logging
    >>> logger = logging.getLogger()
    >>> formatter = JSONFormatter('name message')
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger.addHandler(handler)
    >>> logger.warning('hello world')
    {"name": "root", "message": "hello world"}

    Logging extra fields:

    >>> import logging
    >>> logger = logging.getLogger()
    >>> formatter = JSONFormatter('message extra')
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger.addHandler(handler)
    >>> logger.warning('hello', extra={'extra': 'world'})
    {"message": "hello", "extra": world"}

    Passing args to the message:

    >>> import logging
    >>> logger = logging.getLogger()
    >>> formatter = JSONFormatter('message')
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger.addHandler(handler)
    >>> logger.warning('hello {}', 'world')
    {"message": "hello world"}
    """

    def __init__(
        self,
        fields: Iterable[str] | str | None = None,
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        indent: int = 2,
    ):

        if fields is None:
            self.fields = LOGRECORD_ATTRS
        elif isinstance(fields, str):
            self.fields = tuple(fields.split())
        else:
            try:
                self.fields = tuple(fields)
            except TypeError:
                raise TypeError(
                    "A fields argument must be either None, an iterable or a str."
                )
        self.indent: int = indent
        self.datefmt: str = datefmt

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as a JSON string."""
        # NOTE: it is better to pass args separately in the logger - logger.info('Hello {}', 'world!')
        # than using str.format() or f-strings
        # since the message will be formed only if the logging level is appropriate
        # while strings will be interpolated before logger checks the message's level
        # wasting program time

        # mypy error when assigning to record.message: Type cannot be declared in assignment to non-self attribute
        message: str = record.msg.format(*record.args) if record.args else record.msg
        record.message = message

        datetime_from_num: Callable[
            [float], datetime.datetime
        ] = lambda x: datetime.datetime.fromtimestamp(x)
        asctime: str = f"{datetime_from_num(record.created):{self.datefmt}}"
        record.asctime = asctime

        # fields provided with the use of extra dict are available in record.__dict__
        selection: list[str] = [attr for attr in record.__dict__ if attr in self.fields]
        sort_order: dict[str, int] = {
            field: sort_order for sort_order, field in enumerate(self.fields)
        }
        selection.sort(key=lambda x: sort_order[x])

        log: dict[str, Any] = {attr: getattr(record, attr) for attr in selection}

        return json.dumps(
            log,
            indent=self.indent,
            ensure_ascii=False,  # to avoid printing utf codes for non-ascii characters
        )
