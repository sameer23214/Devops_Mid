import unittest
from app.validation import validate_submission

class TestAssignmentValidation(unittest.TestCase):

    def test_complete_valid_submission(self):
        data = {
            "name": "Sameer Ahmad",
            "regNumber": "FA23-BSE-011",
            "title": "DevOps Lab Midterm",
            "url": "https://github.com/sameer12354we5/bse7_011"
        }
        is_valid, msg = validate_submission(data)
        self.assertTrue(is_valid, f"Expected valid submission, got error: {msg}")

    def test_missing_registration_number(self):
        data = {
            "name": "Sameer Ahmad",
            "regNumber": "",
            "title": "DevOps Lab Midterm",
            "url": "https://github.com/sameer12354we5/bse7_011"
        }
        is_valid, msg = validate_submission(data)
        self.assertFalse(is_valid, "Expected rejection due to missing registration number")

    def test_invalid_submission_url(self):
        data = {
            "name": "Sameer Ahmad",
            "regNumber": "FA23-BSE-011",
            "title": "DevOps Lab Midterm",
            "url": "not-a-valid-url"
        }
        is_valid, msg = validate_submission(data)
        self.assertFalse(is_valid, "Expected rejection due to invalid submission URL")

if __name__ == "__main__":
    unittest.main()
