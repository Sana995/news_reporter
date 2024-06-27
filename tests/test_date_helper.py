import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helpers.date_helper import convert_to_date, get_date_range

class TestDateHelper(unittest.TestCase):

    def test_convert_to_date(self):
        # Test valid date formats
        self.assertEqual(convert_to_date("January 01, 2020"), datetime(2020, 1, 1))
        self.assertEqual(convert_to_date("Jan 01, 2020"), datetime(2020, 1, 1))
        self.assertEqual(convert_to_date("Jan 01 2020"), datetime(2020, 1, 1))
        self.assertEqual(convert_to_date("Sept 01, 2020"), datetime(2020, 9, 1))  # Handle 'Sept' case

    def test_get_date_range(self):
        current_date = datetime.today()

        # Test 0 months
        self.assertEqual(get_date_range(0).date(), current_date.date())

        # Test 1 month
        self.assertEqual(get_date_range(1).date(), (current_date - relativedelta(months=1)).date())

        # Test 2 months
        self.assertEqual(get_date_range(2).date(), (current_date - relativedelta(months=2)).date())

        # Test negative month (should return current date)
        self.assertEqual(get_date_range(-1).date(), current_date.date())


if __name__ == "__main__":
    unittest.main()
