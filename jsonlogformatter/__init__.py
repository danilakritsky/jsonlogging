import datetime
import json
import logging

# https://betterprogramming.pub/4-new-type-annotation-features-in-python-3-11-84e7ec277c29

# https://docs.python.org/3/library/logging.html#logrecord-attributes
LOGRECORD_ATTRS: list[str] = [
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
]


class JSONFormatter:
    """Log formatter object that formats records as JSON strings."""

    def __init__(self, fields=None, datefmt="%Y-%m-%d %H:%M:%S", indent=2):
        """ """
        if fields is None:
            self.fields = LOGRECORD_ATTRS
        else:
            self.fields = fields if isinstance(fields, list) else fields.split()
        self.indent = indent
        self.datefmt = datefmt

    def format(self, record):
        # NOTE: it is better to pass args separately in the logger - logger.info('Hello {}', 'world!')
        # than using str.format() or f-strings
        # since the message will be formed only if the logging level is appropriate
        # while strings will be interpolated before logger checks the message's level
        # wasting program time
        record.message = record.msg.format(*record.args)

        datetime_from_num = lambda x: datetime.datetime.fromtimestamp(x)
        record.asctime = f"{datetime_from_num(record.created):{self.datefmt}}"

        # fields provided with the use of extra dict are available in record.__dict__
        selection = [attr for attr in record.__dict__ if attr in self.fields]
        sort_order = {field: sort_order for sort_order, field in enumerate(self.fields)}
        selection.sort(key=lambda x: sort_order[x])

        log = {attr: getattr(record, attr) for attr in selection}

        return json.dumps(
            log,
            indent=self.indent,
            ensure_ascii=False,  # to avoid printing utf codes for non-ascii characters
        )






