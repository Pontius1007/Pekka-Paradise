# -*- coding utf-8 -*-

import unittest
import ime_data_fetch


class Testerino(unittest.TestCase):

    def test_subject_exists_boolean(self):
        self.assertTrue(ime_data_fetch.subject_exists_boolean("tdt4145"))
        self.assertTrue(ime_data_fetch.subject_exists_boolean("tdt4140"))
        self.assertTrue(ime_data_fetch.subject_exists_boolean("afr1000"))
        self.assertTrue(ime_data_fetch.subject_exists_boolean("klas2003"))
        self.assertFalse(ime_data_fetch.subject_exists_boolean("bull"))
        self.assertFalse(ime_data_fetch.subject_exists_boolean(22))
        self.assertFalse(ime_data_fetch.subject_exists_boolean(""))

    def test_get_subject_name(self):
        self.assertEqual(ime_data_fetch.get_subject_name("tdt4145"), "TDT4145: Data Modelling, Databases "
                                                                     "and Database Management Systems")
        self.assertEqual(ime_data_fetch.get_subject_name("afr1000"), "AFR1000: Introduction to African Studies")
        self.assertEqual(ime_data_fetch.get_subject_name("tdt1234"), 'Subject does not exist')
        self.assertEqual(ime_data_fetch.get_subject_name(10), 'Subject does not exist')

if __name__ == '__main__':
    unittest.main()
