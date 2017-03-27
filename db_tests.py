import unittest
import user_methods


class DbTests(unittest.TestCase):

    def test_user_methods(self):
        user = "Test User1337"
        subject = "TDT4120"
        user_methods.add_user(user, subject)
        self.assertTrue(user_methods.has_user("Test User1337"))
        self.assertEqual(user_methods.get_subject_from_user("Test User1337"), "TDT4120")
        user_methods.add_subject("Test User1337", "TMA4100")
        self.assertEqual(user_methods.get_subject_from_user("Test User1337"), "TMA4100")
        user_methods.delete_user("Test User1337")


if __name__ == '__main__':
    unittest.main()
