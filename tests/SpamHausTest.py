import unittest
import sys

sys.path.append("..")
from spam.SpamHausChecker import SpamHausChecker

class MockSpamHausChecker(SpamHausChecker):
    def set_spam(self, is_spam):
        """docstring for setSpam"""
        self.is_spam = is_spam

    def _resolve(self, domain):
        """docstring for __resolve"""
        if self.is_spam:
            return "2.3.4.5"
        else:
            return "1.2.3.4"

    def _query_spamhaus(self, zone):
        """docstring for __query_spamhaus"""
        if zone.startswith("5.4.3.2"):
            return "127.0.0.2"
        return None

class TestSpamHausChecker(unittest.TestCase):
    def setUp(self):
        self.checker = MockSpamHausChecker()

    def test_spammer(self):
        self.checker.set_spam(True)
        result = self.checker.check_url("http://doevil.com/")
        self.assertEqual(result, MockSpamHausChecker.IS_SPAM)

    def test_innocent(self):
        self.checker.set_spam(False)
        result = self.checker.check_url("http://dogood.com/")
        self.assertEqual(result, MockSpamHausChecker.IS_NOT_SPAM)


if __name__ == '__main__':
    unittest.main()

