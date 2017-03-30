# -*- coding utf-8 -*-
import sys
import unittest
from io import StringIO
import user_methods
import random


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
        user_methods.add_user(user, subject)
        with Capturing() as output:
            user_methods.add_user(user, subject)
        if len(output) > 0:
            self.assertEqual('User already exists', str(output[0]))
        else:
            print("Something went wrong")
        self.assertTrue(user_methods.has_user(user))
        self.assertEqual(user_methods.get_subject_from_user(user), subject)
        test_sub = "TST4" + str(random.randint(0, 2000))
        user_methods.add_subject(user, test_sub)
        self.assertEqual(user_methods.get_subject_from_user(user), test_sub)
        user_methods.delete_user(user)
        self.assertFalse(user_methods.has_user(user))
        user_methods.remove_subject(test_sub)
        self.assertFalse(user_methods.subject_has_subject(test_sub))

        user_methods.add_subject_to_subject_table(test_sub)
        # Test that this works
        user_methods.remove_subject(test_sub)
        # Test that this works

if __name__ == '__main__':
    unittest.main()
