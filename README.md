**Overview**

This project aims to automate the process of extracting news articles from a website, processing the data, and storing it in an Excel file. The script will perform a search, extract relevant details from the latest news articles, download associated images, and save all the information in an organized format. This is only on PoC level, it supports only https://www.latimes.com/. news_bot.png

**Prerequisites**

Python 3.9

Required Python libraries: logger, pandas, Selenium and webdriver...

Check requirements.txt

To run this process, .env_example file should be modified with values and renamed to .env

**Notes**

The web page seems to be dynamic and that is why waits and retries are implemented in scrape methods. From additional features the process has a counter of words in a text and checker for USD amount. At the end, the Excel report is created.

Service for sending emails is a possible addition, method is tested but currently not used.

_Future improvements_

Rewrite helpers into classes to comply with OOP practices

Implement the factory pattern for scrapers, so when you need to scrape another website you just implement the abstract class with custom logic and selectors for that website. 

Improve tests with edge cases and cover the scraper with tests.

Refactor main.py and tasks.py to not repeat code. 

**File Structure**

<pre>
news_reporter/
├── .venv/                     # Virtual environment directory
├── data_models/               # Data models for the project
│   └── article.py             # Data model for news article
├── helpers/                   # Helper functions
│   ├── date_helper.py         # Date-related helper functions
│   ├── parse_data_helper.py   # Data parsing helper functions
│   └── scrape_helper.py       # Web scraping helper functions
├── photos/                    # Directory to store downloaded images
├── reports/                   # Directory to store generated reports
│   └── Report_Money_YYYYMMDD_HHMMSS.xlsx # Output report
├── scrapers/                  # Web scraper modules
│   ├── base_scraper.py        # Base scraper class
│   └── latimes_scraper.py     # Specific scraper for LA Times
├── services/                  # Service modules
│   ├── email_service.py       # Service for sending emails
│   └── excel_report_service.py# Service for generating Excel reports
├── tests/                     # Unit tests for the project
│   ├── test_date_helper.py    # Tests for date helper
│   ├── test_scrape_helpers.py # Tests for scrape helper
│   └── test_text_helpers.py   # Tests for text helper
├── .env                       # Environment variables
├── .env_example               # Example environment variable file
├── .gitignore                 # Git ignore file
├── README.md                  # Project README file
├── main.py                    # Main script to run the bot
└── requirements.txt           # Python dependencies
</pre>
