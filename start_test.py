#!/usr/bin/env python
# encoding: utf-8
import unittest
from utils.config_parser import ConfigData
from redmine.redreq import get_project_data


class ParseConfigTestCase(unittest.TestCase):

    """

    Base test class for test the fields
    of the ConfigFile processed properly.

    """
    def testConfRetrieval(self):
        self.assertEqual(type(ConfigData().url), str)
        self.assertEqual(type(ConfigData().key), str)
        self.assertEqual(type(ConfigData().project), str)

    def testProjectCall(self):
        success, data_or_msg = get_project_data(ConfigData())
        self.assertEqual(success, True)


if __name__ == '__main__':
    unittest.main()