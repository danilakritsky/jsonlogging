from collections import OrderedDict
import logging
import json
import re
import string


class FormatMixin:
    def _format(self, record):
        self.validate()

        selected_fields = OrderedDict()
        for field in self._get_fields():
            selected_fields[field] = record.__dict__[field]

        try:
            if defaults := self._defaults:
                values = defaults | selected_fields
            else:
                values = selected_fields
        except AttributeError:
            values = selected_fields
        return json.dumps(values)


class PercentStyleToJSON(FormatMixin, logging.PercentStyle):

    # https://stackoverflow.com/questions/45772736/python-regex-why-does-findall-find-nothing-but-search-works
    validation_pattern = re.compile(
        r"""
            %\(\w+\)            # ! not a group
            [#0+ -]*
            (?:\*|\d+)?         # non-capturing group
            (?:\.
                (?:\*|\d+)
            )?
            [diouxefgcrsa%]
            """,
        re.I | re.VERBOSE,
    )

    extraction_pattern = re.compile(
        r"""
            %
            \(
                (\w+)        # capturing group
            \)
            [#0+ -]*
            (?:\*|\d+)?
            (?:\.
                (?:\*|\d+)
            )
            ?[diouxefgcrsa%]
            
            """,
        re.I | re.VERBOSE,
    )

    def _get_fields(self):
        return self.extraction_pattern.findall(self._fmt)


class StrFormatStyleToJSON(FormatMixin, logging.StrFormatStyle):
    def validate(self):
        """Validate the input format, ensure it is the correct string formatting style
        Returns all validated fields in order to be used to construct a message.
        """
        fields = self._get_fields()
        if not fields:
            raise ValueError("invalid format: no fields")

    def _get_fields(self):
        fields = OrderedDict()
        try:
            for _, fieldname, spec, conversion in logging._str_formatter.parse(
                self._fmt
            ):
                if fieldname:
                    if not self.field_spec.match(fieldname):
                        raise ValueError(
                            "invalid field name/expression: %r" % fieldname
                        )
                    fields[fieldname] = None
                if conversion and conversion not in "rsa":
                    raise ValueError("invalid conversion: %r" % conversion)
                if spec and not self.fmt_spec.match(spec):
                    raise ValueError("bad specifier: %r" % spec)
        except ValueError as e:
            raise ValueError("invalid format: %s" % e)
        return fields


class StringTemplateStyleToJSON(FormatMixin, logging.StringTemplateStyle):
    def validate(self):
        fields = self._get_fields()
        if not fields:
            raise ValueError("invalid format: no fields")

    def _get_fields(self):
        pattern = string.Template.pattern
        fields = OrderedDict()
        for m in pattern.finditer(self._fmt):
            d = m.groupdict()
            if d["named"]:
                fields[d["named"]] = None
            elif d["braced"]:
                fields[d["braced"]] = None
            elif m.group(0) == "$":
                raise ValueError("invalid format: bare '$' not allowed")
        return fields


_STYLES = {
    "%": (PercentStyleToJSON, logging.BASIC_FORMAT),
    "{": (StrFormatStyleToJSON, "{levelname}:{name}:{message}"),
    "$": (StringTemplateStyleToJSON, "${levelname}:${name}:${message}"),
}


class JSONLogFormatter(logging.Formatter):
    def __init__(
        self, fmt=None, datefmt=None, style="%", validate=False, *, defaults=None,
        indent=2, sort_keys=False
    ):
        # https://stackoverflow.com/questions/61261992/why-super-init-doesnt-have-a-self-reference
        # exception handler to support earlier versions of logging, which had no defaults parameter
        try:
            super().__init__(
                fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults
            )
        except TypeError:
            super().__init__(
                fmt=fmt, datefmt=datefmt, style=style, validate=validate,
            )

        try:
            self._style = _STYLES[style][0](fmt, defaults=defaults)
        except TypeError:
            self._style = _STYLES[style][0](fmt)
        if validate:
            self._style.validate()

        self._fmt = self._style._fmt
        self.datefmt = datefmt
        self.indent = indent
        self.sort_keys = sort_keys

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = json.loads(self.formatMessage(record))
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            s["exc_text"] = record.exc_text
        if record.stack_info:
            s["stack_info"] = self.formatStack(record.stack_info)
        return json.dumps(s, indent=self.indent, sort_keys=self.sort_keys)
