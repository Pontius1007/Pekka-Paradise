# -*- coding utf-8 -*-

import unittest

import requests

from alt import ime_data_fetch, message_split, subject_info


class Testerino(unittest.TestCase):

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
        self.assertEqual(subject_info.printable_schedule(subject_info.get_schedule("tdt123")), "No schedule available")

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
                    single_lecture.extend("")
                lecture_information.append(single_lecture)
        self.assertEqual(subject_info.gather_lecture_information(schedule),
                         lecture_information)
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
        if course['assessment'][0]['codeName'] == 'Skriftlig eksamen':
            info_string = (
            "%s %s\nStudiepoeng: %s\nStudienivå: %s\nVurderingsordning: %s\nKarakter: %s\nEksamensdato: %s" %
            (course['code'], course['name'],
             course['credit'], course['studyLevelName'],
             course['assessment'][0]['codeName'], course['assessment'][0]['gradeRuleSchemeName'],
             course['assessment'][0]['date']))
        else:
            info_string = ("%s %s\nStudiepoeng: %s\nStudienivå: %s\nVurderingsordning: %s\nKarakter: %s" %
                           (course['code'], course['name'],
                            course['credit'], course['studyLevelName'],
                            course['assessment'][0]['codeName'], course['assessment'][0]['gradeRuleSchemeName']))

        self.assertEqual(subject_info.printable_course_info(subject_info.get_course_json("tdt4145")), info_string)

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
        self.assertEqual(message_split.message_split("heidu"), ["heidu"])


if __name__ == '__main__':
    unittest.main()
