import unittest

from numerology_ast import (
    calculate_compatibility,
    calculate_expression_number,
    calculate_life_path,
    calculate_personality_number,
    calculate_soul_number,
)


class NumerologyTestCase(unittest.TestCase):
    def test_life_path(self):
        self.assertEqual(calculate_life_path("1990-08-15"), 6)
        self.assertEqual(calculate_life_path("11/11/1991"), 6)

    def test_expression_number(self):
        self.assertEqual(calculate_expression_number("Alice"), 3)
        self.assertEqual(calculate_expression_number("John"), 2)

    def test_soul_and_personality_numbers(self):
        self.assertEqual(calculate_soul_number("Alice"), 6)
        self.assertEqual(calculate_personality_number("Alice"), 6)

    def test_compatibility(self):
        self.assertGreaterEqual(calculate_compatibility("1990-08-15", "1990-08-15"), 100)


if __name__ == "__main__":
    unittest.main()
