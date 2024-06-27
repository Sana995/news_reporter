import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)


def get_current_page(driver, css_selector):
    """Check current page on webpage"""
    return re.search('^\d+', get_attribute_text(driver, css_selector)).group()


def get_attribute_text(driver, css_selector, retries=10):
    """"Get attribute text by css selector, retry 10 time if retries not specified"""
    for attempt in range(retries):
        try:
            element = driver.find_element(By.CSS_SELECTOR, css_selector)
            return element.text
        except (StaleElementReferenceException, NoSuchElementException):
            time.sleep(1)
        except Exception as e:
            logging.warning(e)
    raise Exception(f"Failed to get element with retry, class: {css_selector}")


def get_srcset_attribute(driver, css_selector, retries=10):
    """Get srcset attribute from webpage by css selector, retry 10 time if retries not specified"""
    for attempt in range(retries):
        try:
            return (driver.find_element(By.CSS_SELECTOR, css_selector)
                    .get_attribute("srcset"))
        except (StaleElementReferenceException, NoSuchElementException) as e:
            time.sleep(1)
            logging.warning(e)
    raise Exception(f"Failed to get srcset attribute with retry")
