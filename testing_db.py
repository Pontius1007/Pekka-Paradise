# -*- coding utf-8 -*-
import sys
import unittest
from io import StringIO
import user_methods


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class DbTests(unittest.TestCase):

    def test_user_methods(self):
        user = "Test User1337"
        subject = "TDT4120"
        # user_methods.add_user(user, subject)
        with Capturing as output:
            user_methods.add_user(user, subject)
        self.assertEqual('User already exists', str(output[0]))
        self.assertEqual(user_methods.get_subject_from_user("Test User1337"), "TDT4120")
        user_methods.add_subject("Test User1337", "TMA4100")
        self.assertEqual(user_methods.get_subject_from_user("Test User1337"), "TMA4100")
        user_methods.delete_user("Test User1337")


if __name__ == '__main__':
    unittest.main()
