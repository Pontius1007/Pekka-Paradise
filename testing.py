# -*- coding utf-8 -*-

import unittest
import ime_data_fetch
import subject_info


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
        self.assertEqual(subject_info.gather_lecture_information(subject_info.get_schedule("exph0004")),
                         lecture_information)
        self.assertEqual(subject_info.gather_lecture_information(subject_info.get_schedule("tdt123")),
                         "No schedule available")

if __name__ == '__main__':
    unittest.main()
