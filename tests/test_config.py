import logging
import unittest

from jsonlogging import dictConfigFromFile, basicConfig

# MOCK BASIC CONFIG var
class testDictConfigFromFile(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()

    def testDictConfigFromFileWorks(self):
        basicConfig()