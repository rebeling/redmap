#!/usr/bin/env python
# encoding: utf-8
import unittest
from utils.config_parser import ConfigData
from redmine.redreq import get_project_data
from utils.transformator import restructure_data
import json


class MainWorkflowTestCase(unittest.TestCase):
    """
        Base test class for ConfigFile processed properly,
        connect to pm-tool and retrieve data, and jsonfy.
    """

    def setUp(self):
        self.cfg = ConfigData()
        self.success, self.data_or_msg = get_project_data(self.cfg)
        self.restructured = restructure_data(self.data_or_msg, self.cfg.project,
                                        '%s' % self.cfg.url + self.cfg.project)

    def testConfRetrieval(self):
        self.assertEqual(type(self.cfg.url), str)
        self.assertEqual(type(self.cfg.key), str)
        self.assertEqual(type(self.cfg.project), str)

    def testProjectCall(self):
        self.assertEqual(self.success, True)

    def testRestructuring(self):
        self.assertEqual('info' in self.restructured, True)
        self.assertEqual('task' in self.restructured, True)
        self.assertEqual('story' in self.restructured, True)

    def testTransformation(self):
        final_data = json.dumps(self.restructured, indent=4, sort_keys=True)
        self.assertEqual(type(final_data), str)


if __name__ == '__main__':
    unittest.main()