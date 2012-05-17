import unittest
import sys
import StringIO

from spam.surbl import *

class MockSurblChecker(SurblChecker):
    def _query_surbl(self, zone):
        if zone.startswith("doevil.com"):
            return "127.0.0.2"
        return None

class TestSurblChecker(unittest.TestCase):
    def setUp(self):
        two = StringIO.StringIO("a.com\nc.nz\ns.it\n")
        three = StringIO.StringIO("qy.sa.com\nu.cc.nz\nii.sss.it\n")
        self.checker = MockSurblChecker(two, three)

    def test_spammer(self):
        result = self.checker.check_url("http://doevil.com/")
        self.assertEqual(result, MockSurblChecker.IS_SPAM)

    def test_innocent(self):
        result = self.checker.check_url("http://dogood.com/")
        self.assertEqual(result, MockSurblChecker.IS_NOT_SPAM)
