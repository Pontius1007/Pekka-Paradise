# -*- coding utf-8 -*-
import sys
import unittest
from io import StringIO
import user_methods
import random
import add_user


class Capturing(list):
    """
    This class is only for helping 'catch' info written to console
    """
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
        Tests the various methods in user_methods.py as described onwards
        :return: 
        """
        self.user = "Test User1337"
        self.subject = "TDT4120"
        self.test_sub = "TST4" + str(random.randint(0, 2000))
        # Checks that added user is added to database with correct subject
        user_methods.add_user(self.user, self.subject)
        with Capturing() as output:
            # Checks that there is some response if user is already in db
            user_methods.add_user(self.user, self.subject)
        if len(output) > 0:  # This should always trigger as long as the DB is initially empty
            self.assertEqual('User already exists', str(output[0]))
        self.assertTrue(user_methods.has_user(self.user))
        self.assertEqual(user_methods.get_subject_from_user(self.user), self.subject)

        # Updates subject for user and checks that it updates in db
        user_methods.add_subject(self.user, self.test_sub)
        self.assertEqual(user_methods.get_subject_from_user(self.user), self.test_sub)
        # Removes user then subject and verifies that they are removed from db
        user_methods.delete_user(self.user)
        self.assertFalse(user_methods.has_user(self.user))
        user_methods.remove_subject(self.test_sub)
        self.assertFalse(user_methods.subject_has_subject(self.test_sub))
        # Adds and removes subject independently from user
        user_methods.add_subject_to_subject_table(self.test_sub)
        self.assertTrue(user_methods.subject_has_subject(self.test_sub))
        user_methods.remove_subject(self.test_sub)
        self.assertFalse(user_methods.subject_has_subject(self.test_sub))

        # Now assume methods for adding and removing subjects and users are working
        # Add new user with subject not in db, just to test
        self.assertFalse(user_methods.subject_has_subject(self.test_sub))
        user_methods.add_user(self.user, self.test_sub)
        self.assertTrue(user_methods.subject_has_subject(self.test_sub))
        user_methods.delete_user(self.user)
        user_methods.remove_subject(self.test_sub)

        # Check that user_methods throws exceptions when given wrong args
        self.assertRaises(Exception, user_methods.has_user(1337))
        self.assertRaises(Exception, user_methods.subject_has_subject(1337))
        self.assertRaises(Exception, user_methods.add_subject_to_subject_table(1337))
        self.assertRaises(Exception, user_methods.get_subject_from_user(1337))
        self.assertRaises(Exception, user_methods.add_user(1337, 1337))
        self.assertRaises(Exception, user_methods.add_subject(1337, 1337))

    def test_add_user(self):
        """
        Tests the small class add_user, assumes user_methods works        
        :return: 
        """
        self.assertFalse(user_methods.has_user(self.user))
        add_user.add_user(self.user, self.test_sub)
        self.assertTrue(user_methods.has_user(self.user))
        self.assertTrue(user_methods.subject_has_subject(self.test_sub))
        user_methods.delete_user(self.user)
        user_methods.remove_subject(self.test_sub)

if __name__ == '__main__':
    unittest.main()
