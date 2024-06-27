import logging
import urllib.request
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from scrapers.base_scraper import BaseScraper
from helpers.date_helper import convert_to_date, get_date_range
from helpers.parse_data_helper import find_keyword_matches, contains_usd_amount
from helpers.scrape_helper import get_srcset_attribute, get_attribute_text, get_current_page
from data_models.article import Article
from services.excel_report_service import write_to_report

class LATimesScraper(BaseScraper):

    def __init__(self):
        self.__scraped_data = []
        self.__flag_scrape_data = True
        self.__counter = 0
        self.__search_word = ""


    def search(self, driver, url: str, search_word: str):
        driver.get(url)
        self.__search_word = search_word
        # Wait for the search button and click it
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-element="search-button"]')
            )
        )
        search_button.click()

        # Wait for the search form input and send keys
        search_form_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-element="search-form-input"]')
            )
        )
        search_form_input.send_keys(self.__search_word)

        # Wait for the search submit button and click it
        search_submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-element="search-submit-button"]')
            )
        )
        search_submit_button.click()

        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "search-results-module-results-menu")
            )
        )
        logging.info("Search finished")

    def set_sort_by_newest(self, driver):
        # Sort by newest
        for retry in range(4):
            try:
                dropdown_element = driver.find_element(By.CLASS_NAME, "select-input")
                select = Select(dropdown_element)
                select.select_by_visible_text("Newest")
                time.sleep(2)
                dropdown_element_check = driver.find_element(By.CSS_SELECTOR, "[selected='selected']").text
                if dropdown_element_check == "Newest":
                    break
            except Exception as e:
                logging.warning(f'Error occured while setting sort by newest: {e}')
                if retry == 4:
                    logging.exception("Failed to set sort by Newest - process is stopped")
                    self.__flag_scrape_data = False
                    raise

    def get_data(self, driver, wanted_time):
        wanted_time = get_date_range(wanted_time)
        while self.__flag_scrape_data:
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "search-results-module-results-menu")
                )
            )
            items = results.find_elements(By.TAG_NAME, "li")
            for index in range(len(items)):
                # First elements index is 1 on the web page
                index += 1
                scraped_time = get_attribute_text(driver,
                                                  f"main > ul > li:nth-child({index}) > ps-promo > div > div.promo-content > p.promo-timestamp")

                # Convert time from string to datetime, so we can compare it to wanted time variable
                if convert_to_date(scraped_time) < wanted_time:
                    # If time is out of defined period by the user, stop scraping data
                    self.__flag_scrape_data = False
                    logging.info('Time limit reached')
                    break
                # Covers cases where there is different text but contains promo-title
                title = get_attribute_text(driver,
                                           f"main > ul > li:nth-child({index}) > ps-promo > div > div.promo-content > div > h3")

                # Handle cases with no description
                try:
                    description = get_attribute_text(driver,
                                                     f"main > ul > li:nth-child({index}) > ps-promo > div > div.promo-content > p.promo-description")
                except NoSuchElementException:
                    description = "Description unavailable"

                no_of_keywords = find_keyword_matches(self.__search_word, title + " " + description)
                flag_amount = contains_usd_amount(title + " " + description)

                try:
                    img_element = get_srcset_attribute(driver, "picture > source")
                    # Get image url
                    img_url = img_element.split(",")[0].split()[0]
                    # Save image to photos folder
                    file_path = f"./photos/{self.__search_word}_{self.__counter}.png"
                    urllib.request.urlretrieve(img_url, file_path)
                except NoSuchElementException:
                    logging.info('No image available')
                    file_path = "No image available"
                    img_url = "No image available"

                logging.debug(
                    f"Index: {index}, Title: {title}, Description: {description}, Time: {scraped_time}, Image URL: {img_url}"
                )

                self.__scraped_data.append(
                    Article(title, description, convert_to_date(scraped_time), file_path, flag_amount,
                            no_of_keywords))
                self.__counter += 1

            # Go to next page if the robot should still scrape data
            if self.__flag_scrape_data:
                for retry in range(4):
                    try:
                        current_page = get_current_page(driver, ".search-results-module-page-counts")
                        logging.debug(f'Current page: {current_page}')

                        # This is hardcoded limit to 10 pages because the page has a limit to 10 pages
                        if int(current_page) == 10:
                            logging.info("Page limit reached")
                            self.__flag_scrape_data = False
                            break

                        next_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, "search-results-module-next-page")
                            )
                        )
                        next_button.click()
                        time.sleep(2)

                        next_page = get_current_page(driver, ".search-results-module-page-counts")
                        if int(current_page) < int(next_page):
                            break
                    except Exception as e:
                        logging.warning(f'Error occured while clicking next page: {e}')
                        if retry == 4:
                            # Stop process if it's not possible to navigate to next page - this would have better handling on production
                            logging.exception("Failed to go to next page - process is stopped")
                            self.__flag_scrape_data = False
                            raise

    def write_data(self):
        logging.debug(f'counter: {self.__counter}')
        write_to_report(self.__scraped_data)
