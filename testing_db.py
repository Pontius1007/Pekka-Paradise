# -*- coding utf-8 -*-
import sys
import unittest
from io import StringIO
import user_methods
import random
import feedback_methods
import datetime
import lecture_methods


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
        user = "Test User1337"
        subject = "TDT4120"
        test_sub = "TST4" + str(random.randint(0, 2000))
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

        # Now assume methods for adding and removing subjects and users are working
        # Add new user with subject not in db, just to test
        self.assertFalse(user_methods.subject_has_subject(test_sub))
        user_methods.add_user(user, test_sub)
        self.assertTrue(user_methods.subject_has_subject(test_sub))
        user_methods.delete_user(user)
        user_methods.remove_subject(test_sub)

        # Check that user_methods throws exceptions when given wrong args
        self.assertRaises(Exception, user_methods.has_user(1337))
        self.assertRaises(Exception, user_methods.subject_has_subject(1337))
        self.assertRaises(Exception, user_methods.add_subject_to_subject_table(1337))
        self.assertRaises(Exception, user_methods.get_subject_from_user(1337))
        self.assertRaises(Exception, user_methods.add_user(1337, 1337))
        self.assertRaises(Exception, user_methods.add_subject(1337, 1337))

    def test_feedback_methods(self):
        """
        This methods tests feedback methods, and assumes user_methods work.
        Starts by adding 'dummy' user and lectures to db and then tests the 
        various, methods in feedback_methods.py.        # subj year(int) week(int) day(int)  start_t end_t  room
        :return: 
        """
        today = self.get_today()
        name = "TESTER LASTNAME"
        lecture_info = ["TST4200"]
        for item in today:
            lecture_info.append(item)
        lecture_info.append("01:00")
        lecture_info.append("24:59")
        lecture_info.append("P")
        # Add user and test lecture
        user_methods.add_user(name, lecture_info[0])
        lecture_methods.add_and_remove_test(False, lecture_info)

        # Checks the various feedback methods
        self.assertTrue(feedback_methods.add_entry(name, lecture_info[0], "1"))
        self.assertFalse(feedback_methods.add_entry(name, lecture_info[0], "0"))
        feedback_methods.remove_all_feedback(name)
        # Add method to add feedback evaluation stuff
        self.assertTrue(feedback_methods.add_entry(name, lecture_info[0], "1"))
        feedback, feedbackevaluation = feedback_methods.get_all_subject_feed(lecture_info[0])
        self.assertEqual(feedback, [1])

        # Remove user, test feedback and lecture
        feedback_methods.remove_all_feedback(name)
        user_methods.delete_user(name)
        user_methods.remove_subject(lecture_info[0])
        lecture_methods.add_and_remove_test(True, lecture_info)

    @staticmethod
    def get_today():
        """
        Returns year, week and day.
        :return: [year, week, day]
        """
        date = datetime.date.today()
        return [date.year, datetime.date.isocalendar(date)[1], datetime.datetime.today().weekday() + 1]

if __name__ == '__main__':
    unittest.main()
