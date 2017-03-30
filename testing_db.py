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
        """
        Tests the various methods in user_methods.py
        :return: 
        """
        user = "Test User1337"
        subject = "TDT4120"
        # Checks that added user is added to database with correct subject
        user_methods.add_user(user, subject)
        with Capturing() as output:
            # Checks that there is some response if user is already in db
            user_methods.add_user(user, subject)
        if len(output) > 0:  # This should always trigger as long as the DB is initially empty
            self.assertEqual('User already exists', str(output[0]))
        self.assertTrue(user_methods.has_user(user))
        self.assertEqual(user_methods.get_subject_from_user(user), subject)

        # Updates subject for user and checks that it updates in db
        test_sub = "TST4" + str(random.randint(0, 2000))
        user_methods.add_subject(user, test_sub)
        self.assertEqual(user_methods.get_subject_from_user(user), test_sub)
        # Removes user then subject and verifies that they are removed from db
        user_methods.delete_user(user)
        self.assertFalse(user_methods.has_user(user))
        user_methods.remove_subject(test_sub)
        self.assertFalse(user_methods.subject_has_subject(test_sub))
        # Adds and removes subject independently from user
        user_methods.add_subject_to_subject_table(test_sub)
        self.assertTrue(user_methods.subject_has_subject(test_sub))
        user_methods.remove_subject(test_sub)
        self.assertFalse(user_methods.subject_has_subject(test_sub))


if __name__ == '__main__':
    unittest.main()
