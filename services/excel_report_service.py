import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from datetime import date

load_dotenv()
search_word = os.environ["SEARCH_WORD"]

def write_to_report(data):
    """Write scraped data to excel report file"""
    # Convert the scraped data to a list of dictionaries
    data_dicts = [
        {
            "Title": article.title,
            "Description": article.description,
            "Date": article.date,
            "File Path": article.file_path,
            "Flag Amount": article.flag_amount,
            "Number of Keywords": article.no_of_keywords,
        }
        for article in data
    ]

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_dicts)

    reports_dir = './reports'
    os.makedirs(reports_dir, exist_ok=True)
    file_name = f"{reports_dir}/Report_{search_word}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    # Write the DataFrame to an Excel file
    df.to_excel(file_name, index=False)

    logging.info(f"Data successfully written to {file_name}")



# data = {
#     "Title": "Jenni Rivera’s family battles over singer’s estate. ‘Money, power, greed’ tear them apart",
#     "Date": datetime(2024, 6, 26, 0, 0),
#     "Description": "It’s been nearly a dozen years since Jenni Rivera, an icon of regional Mexican music, perished in a tragic plane crash. But the battle over her legacy is far from over.",
#     "File Path": "./photos/Money_0.png",
#     "Flag Amount": False,
#     "Number of Keywords": 1
# }
# write_to_report(data)