import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

from analyzer import analyze_password


class PasswordAnalyzerTests(unittest.TestCase):

    def test_empty_password(self):
        result = analyze_password("")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["length"], 0)

    def test_weak_password(self):
        result = analyze_password("123456")
        self.assertEqual(result["strength"], "Very Weak")
        self.assertGreater(len(result["warnings"]), 0)

    def test_common_password(self):
        result = analyze_password("password123")
        self.assertLessEqual(result["score"], 20)
        self.assertGreater(len(result["warnings"]), 0)

    def test_stronger_password(self):
        result = analyze_password("BlueTiger!47Cloud")
        self.assertGreaterEqual(result["score"], 70)
        self.assertGreater(result["entropy"], 50)

    def test_uppercase_check(self):
        result = analyze_password("lowercase123!")
        uppercase_check = next(
            check for check in result["checks"]
            if check["name"] == "Uppercase letter"
        )
        self.assertFalse(uppercase_check["passed"])

    def test_special_character_check(self):
        result = analyze_password("Password123")
        special_check = next(
            check for check in result["checks"]
            if check["name"] == "Special character"
        )
        self.assertFalse(special_check["passed"])


if __name__ == "__main__":
    unittest.main()