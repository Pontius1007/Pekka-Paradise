# -*- coding utf-8 -*-
import sys
from io import StringIO

from sqlalchemy.exc import SQLAlchemyError

import user_methods
import random
import feedback_methods
import datetime
import lecture_methods
import unittest
import requests
import message_split
import ime_data_fetch
import subject_info


class Capturing(list):
    """
    This class is for helping 'catch' or read text written to console
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class IMETest(unittest.TestCase):

    def test_subject_exists_boolean(self):
        """
        This method tests the subject_exists_boolean method in ime_data_fetch.py
        """
        self.assertTrue(ime_data_fetch.subject_exists_boolean("tdt4145"))
        self.assertTrue(ime_data_fetch.subject_exists_boolean("tdt4140"))
        self.assertTrue(ime_data_fetch.subject_exists_boolean("afr1000"))
        self.assertTrue(ime_data_fetch.subject_exists_boolean("klas2003"))
        self.assertFalse(ime_data_fetch.subject_exists_boolean("bull"))
        self.assertFalse(ime_data_fetch.subject_exists_boolean(22))
        self.assertFalse(ime_data_fetch.subject_exists_boolean(""))

    def test_get_subject_name(self):
        """
        This method tests the get_subject_name method in ime_data_fetch.py
        """
        self.assertEqual(ime_data_fetch.get_subject_name("tdt4145"), "TDT4145: Data Modelling, Databases "
                                                                     "and Database Management Systems")
        self.assertEqual(ime_data_fetch.get_subject_name("afr1000"), "AFR1000: Introduction to African Studies")
        self.assertEqual(ime_data_fetch.get_subject_name("tdt1234"), 'Subject does not exist')
        self.assertEqual(ime_data_fetch.get_subject_name(10), 'Subject does not exist')

    def test_get_schedule(self):
        """
        This method tests the get_schedule method in subject_info.py
        """
        self.assertEqual(subject_info.get_schedule("tdt4145")['course']['summarized'][0]['acronym'], "FOR")
        self.assertEqual(subject_info.get_schedule("tdt4100")['course']['summarized'][0]['acronym'], "LAB")
        self.assertFalse(subject_info.get_schedule("tdt123"))
        self.assertFalse(subject_info.get_schedule(123))
        self.assertFalse(subject_info.get_schedule("tdt4120"))

    def test_printable_schedule(self):
        """
        This method test the printable_schedule method in subject_info.py
        """
        week = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag"]
        test_schedule = subject_info.get_schedule("tdt4145")['course']['summarized']
        schedule_string = "Timeplan for " + test_schedule[0]['courseName'] + ":\n"
        for i in range(0, len(test_schedule)):
            schedule_string += (test_schedule[i]['description'] + " "
                                + week[test_schedule[i]['dayNum'] - 1] +
                                " fra " + test_schedule[i]['from'] +
                                " til " + test_schedule[i]['to'] + "\n")
        self.assertEqual(subject_info.printable_schedule(subject_info.get_schedule("tdt4145")), schedule_string)
        self.assertEqual(subject_info.printable_schedule(subject_info.get_schedule("tdt123")), "No schedule available.")

    def test_gather_lecture_information(self):
        """
        This method tests the gather_lecture_information method in subject_info.py
        a schedule is created in this method and is then compared to that
        created by the call to gather_lecture__information
        Possibly problematic: the call to get_schedule will not always return a schedule in the same order
        (returns a schedule with the same elements but not always ordered similarly),
         hotfixed by using only 1 call to get schedule instead of 2
        """
        lecture_information = []

        schedule = subject_info.get_schedule("exph0004")
        for i in range(0, len(schedule['course']['summarized'])):
            if schedule['course']['summarized'][i]['acronym'] == 'FOR':
                single_lecture = []
                single_lecture.extend(
                    (schedule['course']['summarized'][i]['courseCode'], schedule['course']['summarized'][i]['from'],
                     schedule['course']['summarized'][i]['to'], schedule['course']['summarized'][i]['dayNum'],
                     schedule['course']['summarized'][i]['weeks'], schedule['course']['summarized'][i]['arsterminId']))
                try:
                    single_lecture.extend(schedule['course']['summarized'][i]['rooms'][0]['romNavn'])
                except IndexError:
                    single_lecture.extend("None")
                lecture_information.append(single_lecture)
        self.assertEqual(subject_info.gather_lecture_information(schedule), lecture_information)
        self.assertEqual(subject_info.gather_lecture_information(subject_info.get_schedule("tdt123")),
                         "No schedule available")

    def test_get_course_json(self):
        """
        This method tests the get_course_json method in subject_info.py
        """
        self.assertEqual(subject_info.get_course_json("tdt123"), 'Subject does not exist')
        self.assertEqual(subject_info.get_course_json(420), 'Subject does not exist')
        course = requests.get("http://www.ime.ntnu.no/api/course/tdt4145").json()
        self.assertEqual(subject_info.get_course_json("tdt4145"), course)

    def test_printable_course_info(self):
        """
        This method tests the printable_course_info method in subject_info.py
        """
        self.assertEqual(subject_info.printable_course_info(subject_info.get_course_json("tdt123")),
                         'subject does not exist and thus has no information')
        self.assertEqual(subject_info.printable_course_info(subject_info.get_course_json(0)),
                         'subject does not exist and thus has no information')

        # creates a similar info string for comparison
        course = subject_info.get_course_json("tdt4145")
        course = course['course']
        info_string = (
            "%s %s\nStudiepoeng: %s\nStudienivå: %s\nVurderingsordning: %s\nKarakter: %s\nEksamensdato: %s" %
            (course['code'], course['name'],
             course['credit'], course['studyLevelName'],
             course['assessment'][0]['codeName'], course['assessment'][0]['gradeRuleSchemeName'],
             course['assessment'][0]['date']))

        self.assertEqual(subject_info.printable_course_info(subject_info.get_course_json("tdt4145")), info_string)

        course = subject_info.get_course_json("tdt4140")
        course = course['course']
        info_string = ("%s %s\nStudiepoeng: %s\nStudienivå: %s\nVurderingsordning: %s\nKarakter: %s" %
                       (course['code'], course['name'],
                        course['credit'], course['studyLevelName'],
                        course['assessment'][0]['codeName'],
                        course['assessment'][0]['gradeRuleSchemeName']))
        self.assertEqual(subject_info.printable_course_info(subject_info.get_course_json("tdt4140")), info_string)

    def test_course_name(self):
        """
        This method tests the course_name method in subject_info.py
        """

        self.assertEqual(subject_info.course_name("tdt4100"), "Objektorientert programmering")
        self.assertEqual(subject_info.course_name("tdt4120"), "Algoritmer og datastrukturer")
        self.assertEqual(subject_info.course_name("shallabais"), "Subject does not exist")
        self.assertEqual(subject_info.course_name(1234), "Subject does not exist")

    def test_message_split(self):
        """
        This method tests the message_split method in message_split.py
        """
        tekst1 = "a" * 50
        tekst2 = "b" * 50
        melding = ""

        for i in range(20):
            if i % 2 == 0:
                melding += tekst1 + "\n"
            else:
                melding += tekst2 + "\n"
        msg_list = ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n']
        self.assertEqual(message_split.message_split(melding), msg_list)

        melding = ""

        for i in range(40):
            if i % 2 == 0:
                melding += tekst1 + "\n"
            else:
                melding += tekst2 + "\n"

        msg_list = ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'
                    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n']

        self.assertEqual(message_split.message_split(melding), msg_list)
        self.assertEqual(message_split.message_split("heidu"), ["heidu"])


class UserMethodTests(unittest.TestCase):

    def setUp(self):
        """
        Sets the test values which are sent to the database
        :return:
        """
        self.user = "Test User1337"
        self.subject = "TDT4120"
        self.test_sub = "TST4" + str(random.randint(0, 2000))

    def test_user_methods(self):
        """
        Tests the various methods in user_methods.py as described onwards
        """
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


class FeedbackMethodsTest(unittest.TestCase):

    def setUp(self):
        """
        Populates the database with various test data
        """
        self.today = self.get_today()
        self.name = "TESTER LAST_NAME"
        self.test_sub = "TST4" + str(random.randint(0, 2000))
        self.lecture_info = ["TST4200"]
        for item in self.today:
            self.lecture_info.append(item)
        self.lecture_info.append("01:00")
        self.lecture_info.append("24:59")
        self.lecture_info.append("P")
        user_methods.add_user(self.name, self.lecture_info[0])
        lecture_methods.add_and_remove_test(False, self.lecture_info)

    def test_feedback_methods(self):
        """
        Tests feedback methods, and assumes user_methods work.
        lecture info : [subject(str), year(int), week(int), day(int), start_time(str), end_time(str), room(str)]
        """
        # Checks the various feedback methods
        # Checks the various feedback methods
        self.assertTrue(feedback_methods.add_entry(self.name, self.lecture_info[0], "1"))
        self.assertFalse(feedback_methods.add_entry(self.name, self.lecture_info[0], "0"))
        feedback_methods.remove_all_feedback(self.name)

        self.assertTrue(lecture_methods.check_lecture_in_db(self.lecture_info[0]))
        self.assertFalse(lecture_methods.check_lecture_in_db("TDT420"))
        self.assertFalse(lecture_methods.check_lecture_in_db(self.test_sub))
        self.assertTrue(feedback_methods.add_entry(self.name, self.lecture_info[0], "1"))
        self.assertEqual(feedback_methods.get_single_lecture_feed(self.lecture_info[1], self.lecture_info[2],
                                                                  self.lecture_info[3], self.lecture_info[0])[1], [1])
        self.assertTrue(feedback_methods.user_can_give_feedback_evaluation(self.name, self.lecture_info[0]))
        self.assertTrue(feedback_methods.add_feedback_evaluation(self.name, self.lecture_info[0], 5, 5, 5, 5, 5, 5, 5))
        self.assertFalse(feedback_methods.user_can_give_feedback_evaluation(self.name, self.lecture_info[0]))
        self.assertFalse(feedback_methods.user_can_give_feedback_evaluation(self.name, "TDT420"))
        self.assertFalse(feedback_methods.add_feedback_evaluation(self.name, self.lecture_info[0], 5, 5, 5, 7, 5, 5, 5))
        feedback, feedback_evaluation = feedback_methods.get_all_subject_feed(self.lecture_info[0])
        self.assertEqual(feedback, [1])
        self.assertEqual(feedback_evaluation[0], [5, 5, 5, 5, 5, 5, 5])
        self.assertEqual(
            feedback_methods.get_single_lecture_feedback_questions(
                self.lecture_info[1], self.lecture_info[2], self.lecture_info[3], self.lecture_info[0])[0],
            [5, 5, 5, 5, 5, 5, 5])
        # TODO not everything is tested here
        self.assertFalse(feedback_methods.add_feedback_evaluation(self.name, self.lecture_info[0], 6, 7, 7, 6, 6, 6, 7))

    def tearDown(self):
        """
        Removes test data from the database if it exists
        """
        try:
            feedback_methods.remove_all_feedback(self.name)
        except SQLAlchemyError:
            print("No feedback in db")
        try:
            lecture_methods.add_and_remove_test(True, self.lecture_info)
        except SQLAlchemyError:
            print("No test lecture in db")
        try:
            user_methods.delete_user(self.name)
        except SQLAlchemyError:
            print("No user in db")
        try:
            user_methods.remove_subject(self.lecture_info[0])
        except SQLAlchemyError:
            print("No subject in db")

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
