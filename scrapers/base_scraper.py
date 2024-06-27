from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def search(self, driver, url: str, search_word: str):
        """Search the keyword on the website"""
        pass

    @abstractmethod
    def set_sort_by_newest(self, driver):
        """Set sort filter to Newest"""
        pass

    @abstractmethod
    def get_data(self, driver, wanted_time):
        """Scrape data for an article summary, get title, description, date and image"""
        pass

    @abstractmethod
    def write_data(self):
        """Write scraped data to excel report file"""
        pass
