import unittest
from unittest.mock import MagicMock, patch
import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)
from helpers.scrape_helper import get_current_page, get_attribute_text, get_srcset_attribute


class TestScrapeHelpers(unittest.TestCase):

    @patch('helpers.scrape_helper.get_attribute_text')
    def test_get_current_page(self, mock_get_attribute_text):
        # Mock the return value of get_attribute_text
        mock_get_attribute_text.return_value = "5 of 10 pages"
        driver = MagicMock()
        css_selector = "div.page-info"

        result = get_current_page(driver, css_selector)

        mock_get_attribute_text.assert_called_once_with(driver, css_selector)
        self.assertEqual(result, "5")

    @patch('time.sleep', return_value=None)
    def test_get_attribute_text(self, mock_sleep):
        driver = MagicMock()
        css_selector = "div.content"

        # Create a mock element with text
        mock_element = MagicMock()
        mock_element.text = "Sample Text"

        # Set up the driver to return the mock element
        driver.find_element.return_value = mock_element

        result = get_attribute_text(driver, css_selector)

        driver.find_element.assert_called_with(By.CSS_SELECTOR, css_selector)
        self.assertEqual(result, "Sample Text")

        # Test with exceptions
        driver.find_element.side_effect = [NoSuchElementException, StaleElementReferenceException, mock_element]

        result = get_attribute_text(driver, css_selector)

        self.assertEqual(driver.find_element.call_count, 4)
        self.assertEqual(result, "Sample Text")

    @patch('time.sleep', return_value=None)
    def test_get_srcset_attribute(self, mock_sleep):
        driver = MagicMock()
        css_selector = "img.picture"

        # Create a mock element with srcset attribute
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "image1.jpg 1x, image2.jpg 2x"

        # Set up the driver to return the mock element
        driver.find_element.return_value = mock_element

        result = get_srcset_attribute(driver, css_selector)

        driver.find_element.assert_called_with(By.CSS_SELECTOR, css_selector)
        self.assertEqual(result, "image1.jpg 1x, image2.jpg 2x")

        # Test with exceptions
        driver.find_element.side_effect = [NoSuchElementException, StaleElementReferenceException, mock_element]

        result = get_srcset_attribute(driver, css_selector)

        self.assertEqual(driver.find_element.call_count, 4)
        self.assertEqual(result, "image1.jpg 1x, image2.jpg 2x")


if __name__ == "__main__":
    unittest.main()
