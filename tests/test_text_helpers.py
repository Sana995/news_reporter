import unittest
from helpers.parse_data_helper import find_keyword_matches, contains_usd_amount


class TestTextHelpers(unittest.TestCase):

    def test_find_keyword_matches(self):
        # Test exact match
        self.assertEqual(find_keyword_matches("test", "This is a test."), 1)
        self.assertEqual(find_keyword_matches("test", "test test test"), 3)

        # Test case-insensitive match
        self.assertEqual(find_keyword_matches("test", "Test TEST test"), 3)

        # Test no match
        self.assertEqual(find_keyword_matches("hello", "This is a test."), 0)

    def test_contains_usd_amount(self):
        # Test valid USD amounts
        self.assertTrue(contains_usd_amount("The amount is $100."))
        self.assertTrue(contains_usd_amount("The amount is $1,000.50."))
        self.assertTrue(contains_usd_amount("The amount is 100 dollars."))
        self.assertTrue(contains_usd_amount("The amount is 100 USD."))

        # Test invalid USD amounts
        self.assertFalse(contains_usd_amount("The amount is 100 euros."))
        self.assertFalse(contains_usd_amount("The amount is 100."))
        self.assertFalse(contains_usd_amount("The amount is 1000."))

        # Test no amount
        self.assertFalse(contains_usd_amount("There is no amount mentioned here."))


if __name__ == "__main__":
    unittest.main()
