import json
import logging
import unittest
from io import StringIO

from jsonlogging import LOGRECORD_ATTRS, JSONFormatter

# pytest failes to capture logs
# https://github.com/pytest-dev/pytest/issues/5997


class TestJSONFormatter(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("test")
        self.logger.setLevel(logging.DEBUG)
        self.stdout = StringIO()
        self.handler = logging.StreamHandler(self.stdout)
        self.logger.addHandler(self.handler)

    def stdoutToJSON(self):
        return json.loads(self.stdout.getvalue())

    def testFormatterWorks(self):
        # handler object and handler in logger.handlers
        # refer to the same object
        # thus we can change formatter of the handler object
        # and logger will pick it up
        self.handler.setFormatter(JSONFormatter("message"))
        self.logger.info("hello world")
        self.assertEqual(self.stdoutToJSON(), {"message": "hello world"})

    def testAddingExtraArgsWorks(self):
        self.handler.setFormatter(JSONFormatter("message extra_arg"))
        self.logger.info("hello", extra={"extra_arg": "world"})
        self.assertEqual(
            self.stdoutToJSON(), {"message": "hello", "extra_arg": "world"}
        )

    def testFormattingMessageWithArgsWorks(self):
        self.handler.setFormatter(JSONFormatter("message"))
        self.logger.info("hello {}", "world")
        self.assertEqual(self.stdoutToJSON(), {"message": "hello world"})

    def testIfNoFieldsAreSpecifiedLogAllFields(self):
        self.handler.setFormatter(JSONFormatter(fields=None))
        self.logger.info("hello world")
        self.assertEqual(tuple(self.stdoutToJSON().keys()), LOGRECORD_ATTRS)

    def testPassingIterabletoFieldsWorks(self):
        self.handler.setFormatter(JSONFormatter(["name", "message"]))
        self.logger.info("hello world")
        self.assertEqual(
            self.stdoutToJSON(), {"name": "test", "message": "hello world"}
        )

    def testTypeErrorIsRaisedWhenInvalidTypeIsPassedToFields(self):
        with self.assertRaises(TypeError):
            self.handler.setFormatter(JSONFormatter(1))
