import unittest
from pathlib import Path

from jsonlogging.config import dictConfigFromFile


class TestDictConfigFromFile(unittest.TestCase):
    def setUp(self):
        self.path = Path.cwd()
        self.filename = "jsondictconfig.py"
        self.fullpath = self.path / self.filename

    def testCreatesConfigFileIfItDoesNotExist(self):
        dictConfigFromFile(self.path)
        self.assertTrue(self.fullpath.exists())

    # def testIfFileExistsReturnConfigDict(self):
    #     dictConfigFromFile(self.path)
    #     configdict = dictConfigFromFile(self.fullpath)
    #     self.assertEqual(configdict, str({'config': True}))

    # def tearDown(self):
    #     self.fullpath.unlink()
