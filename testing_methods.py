# -*- coding utf-8 -*-
import sys
from io import StringIO

from sqlalchemy.exc import SQLAlchemyError
from app import responses

import json
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
        del self._stringio  # free up some memory
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


class ResponsesTest(unittest.TestCase):
    """
    This class test that the various templates in responses.py are generated correctly 
    when given data. It works by feeding data into 'template generators' then asserting
    that the correct data is in the following output template.
    """
    def test_greeting(self):
        test_data = json.dumps({
            "recipient": {"id": 1337},
            "message": {"text": "Hello " + "TEST" + "!\nWhat can I do for you today?" +
                                "\nIf you are new to the bot and would like some help, please press 'Help' in chat"}})
        return_data = responses.greeting_message(1337, "TEST USER")
        self.assertEqual(test_data, return_data)

    def test_text(self):
        test_data = json.dumps({
            "recipient": {"id": 12345678},
            "message": {"text": "THIS IS A TEST MESSAGE"}})
        return_data = responses.text_message(12345678, "THIS IS A TEST MESSAGE")
        self.assertEqual(test_data, return_data)

    def test_user_info(self):
        message = "Hello " + "TESTER" + "!\nYou currently have " + "TST420" + " selected"
        test_data = json.dumps({
            "recipient": {"id": 123456789},
            "message": {"text": message}})
        return_data = responses.user_info(123456789, "TESTER", "TST420")
        self.assertEqual(test_data, return_data)

    def test_all_feedback_speed(self):
        url_slow = ["http://www.bbcactive.com/BBCActiveIdeasandResources/Tenwaystomakelecturesmoredynamic.aspx",
                    "http://www.bbcactive.com/BBCActiveIdeasandResources/Tenwaystomakelecturesmoredynamic.aspx",
                    "https://www.missouristate.edu/chhs/4256.htm"]
        url_fast = ["https://tomprof.stanford.edu/posting/491",
                    "www.montana.edu%2Ffacultyexcellence%2FPapers%2Flecture.pdf&h=ATOoZvoecXZQokiY2ApCWeP4lMK1h-aZIF3"
                    "rC6XU_dOtRdx4vBn9fBEcSJMA3i40D5P-QOrdve6qFCxX6rD1MhNwD7VkXnYpyhMRJD8RFnR6zc35vSjRjOBXh0G5ag5C"
                    "K3zQd1WkxbY98LjG1nQo18bAc0I",
                    "http://www.bbcactive.com/BBCActiveIdeasandResources/Tenwaystomakelecturesmoredynamic.aspx"]

        test_data1 = json.dumps({
            "recipient": {"id": 4200},
            "message": {"text": "Feedback for " + "TST4200" + ":\n" +
                                "Total number of participants: " + str(100) + "\n"
                                + str(10) + "% of participants thinks the lectures are too slow.\n"
                                + str(80) + "% of participants thinks the lectures are OK.\n"
                                + str(10) + "% of participants thinks the lectures are too fast.\n\n" +
                                "Your students are happy and you are doing a good job, keep it up!"
                        }
        })

        self.assertEqual(responses.all_feedback_speed(4200, "TST4200", [10, 80, 10, 100]), test_data1)
        self.assertTrue(
            json.loads(responses.all_feedback_speed(4200, "TST4200", [80, 10, 10, 100]))["message"]["text"].split()[-1]
            in url_slow)
        self.assertTrue(
            json.loads(responses.all_feedback_speed(4200, "TST4200", [10, 10, 80, 100]))["message"]["text"].split()[-1]
            in url_fast)

    def test_all_feedback_questions(self):
        test_data = ['1331', '1332', '1333', '1334', '1335', '1336', '1337']
        tst_id = 123
        test_in_generated_data = 0
        generated_text = json.loads(
            responses.all_feedback_questions(tst_id, "TDT420", test_data))["message"]["text"].split()

        for word in generated_text:
            if word in test_data:
                test_in_generated_data += 1

        self.assertTrue(test_in_generated_data == 7)
        self.assertEqual(json.loads(responses.all_feedback_questions(tst_id, "TDT420", test_data))["recipient"]["id"],
                         tst_id)

    def test_no_course(self):
        wanted_string = "You have not chosen a subject \n What would you like to do?:"
        tst_id = 321

        self.assertEqual(json.loads(responses.no_course(tst_id))["message"]["text"], wanted_string)
        self.assertEqual(json.loads(responses.no_course(tst_id))["recipient"]["id"], tst_id)

    def test_has_course(self):
        test_course = "TDT4140"
        user_id = 1337

        self.assertEqual(json.loads(responses.has_course(user_id, test_course))["recipient"]["id"], user_id)
        self.assertEqual(json.loads(responses.has_course(user_id, test_course))["message"]["text"].split()[3:5][1],
                         "Software")

    def test_lec_feed(self):
        tst_id = 321123
        wanted_string = "How do you think this lecture is going:"

        self.assertEqual(json.loads(responses.lec_feed(tst_id))["message"]["text"], wanted_string)
        self.assertEqual(json.loads(responses.lec_feed(tst_id))["recipient"]["id"], tst_id)

    def test_lecture_feedback_questions(self):
        tst_id = 3211

        json_data = json.loads(responses.lecture_feedback_questions(tst_id, "FirstText TextAfterSplit"))
        self.assertEqual(json_data["message"]["text"], "How organized was the lecture?")
        self.assertEqual(json_data["recipient"]["id"], tst_id)

    def test_give_feedback_choice(self):
        json_data = json.loads(responses.give_feedback_choice(13337))

        self.assertEqual(json_data["recipient"]["id"], 13337)
        self.assertEqual(json_data["message"]["text"], "What kind of feedback do want to give?")

    def test_get_feedback_spec_or_all(self):
        json_data = json.loads(responses.get_feedback_specific_or_all(1333))

        self.assertEqual(json_data["recipient"]["id"], 1333)
        self.assertEqual(json_data["message"]["text"], "Do you want feedback from all the lectures or a specific "
                                                       "lecture?")

    def test_get_feedback_year(self):
        json_data = json.loads(responses.get_feedback_year(123456, [2017, 2018]))

        self.assertEqual(json_data["recipient"]["id"], 123456)
        self.assertEqual(json_data["message"]["text"], "Select what year you want feedback from")

    def test_get_feedback_semester(self):
        test_id = 420
        test_year = 240
        test_semester = ["Semester"]

        json_data = json.loads(responses.get_feedback_semester(test_id, test_year, test_semester))
        self.assertEqual(json_data["recipient"]["id"], test_id)
        self.assertEqual(json_data["message"]["text"], "Select what semester you want feedback from")

    def test_get_feedback_month(self):
        test_id = 421
        test_year = '241'
        test_weeks = [123, 125, 126, 127]

        self.assertEqual(
            json.loads(responses.get_feedback_month(test_id, test_year, [123, 122]))["recipient"]["id"], test_id)
        self.assertEqual(
            json.loads(responses.get_feedback_month(test_id, test_year, test_weeks))["message"]["text"],
            "Select what weeks you want feedback from:")

    def test_get_feedback_week(self):
        test_id = 4200
        test_year = '2400'
        test_weeks = [123, 125, 126, 127]

        json_data = json.loads(responses.get_feedback_week(test_id, test_year, test_weeks))
        self.assertEqual(json_data["recipient"]["id"], test_id)
        self.assertEqual(json_data["message"]["text"], "Select what week you want feedback from:")

    def test_get_feedback_day(self):
        test_year = '1234'
        test_week = '123'
        test_id = 1235456
        test_days = [0, 2, 3]

        json_data = json.loads(responses.get_feedback_day(test_id, test_year, test_days, test_week))
        self.assertEqual(json_data["recipient"]["id"], test_id)
        self.assertEqual(json_data["message"]["text"], "Select what day you want feedback from")

    def test_present_lecture_feedback(self):
        test_id = 11232
        feedback_test = ['TST420', [1, 1, 1, 1, 1, 1, 1, 2, 2, 2]]

        json_data = json.loads(responses.present_single_lecture_feedback(test_id, feedback_test))
        self.assertEqual(json_data["message"]["text"].split()[3], str(len(feedback_test[1])))
        self.assertEqual(json_data["message"]["text"].split()[18], '70%')

    def test_present_lecture_questions(self):
        test_id = 33333
        test_feedback = [34, 69, 34, 12, 124, 234, 235]

        json_data = json.loads(responses.present_single_lecture_feedback_questions(test_id, test_feedback))
        self.assertEqual(json_data["message"]["text"].split()[10], str(test_feedback[1]))
        self.assertEqual(json_data["message"]["text"].split()[-1], str(test_feedback[-1]))

if __name__ == '__main__':
    unittest.main()
