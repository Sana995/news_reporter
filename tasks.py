import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scrapers.latimes_scraper import LATimesScraper

from robocorp.tasks import task

load_dotenv()


@task
def minimal_task():
    url = os.environ["URL"]
    search_word = os.environ["SEARCH_WORD"]
    period = 1
    log_level = os.environ["LOG_LEVEL"]

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Configure logging
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    # Set up Selenium Webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    try:
        la_scraper = LATimesScraper()
        la_scraper.search(driver, url, search_word)
        la_scraper.set_sort_by_newest(driver)
        la_scraper.get_data(driver, period)
        la_scraper.write_data()
    finally:
        driver.quit()
        logger.info("Chrome is closed")
