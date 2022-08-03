import json
import logging
import unittest
from io import StringIO
from pathlib import Path

from jsonlogging import JSONFormatter, basicConfig


class testBasicConfig(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.logpath = Path(__name__).parent / "jsonlogging.log"

    def testBasicConfigWorks(self):
        basicConfig()
        self.assertTrue(isinstance(self.logger.handlers[0], logging.StreamHandler))
        self.assertTrue(isinstance(self.logger.handlers[1], logging.FileHandler))
        self.assertTrue(isinstance(self.logger.handlers[1].formatter, JSONFormatter))
        self.assertTrue(self.logpath.exists())

    def tearDown(self):
        self.logpath.unlink()
