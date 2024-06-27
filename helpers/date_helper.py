from datetime import datetime
from dateutil.relativedelta import relativedelta


# List of possible date formats
date_formats = ["%B %d, %Y", "%b %d, %Y", "%b %d %Y"]


def convert_to_date(date_string: str):
    """Converts string to datetime object"""
    cleaned_date_string = date_string.replace(".", "")
    # Handle edge case - September is only month that is not writen in date supported format on the web page
    cleaned_date_string = cleaned_date_string.replace("Sept", "Sep")
    for date_format in date_formats:
        try:
            return datetime.strptime(cleaned_date_string, date_format)
        except ValueError:
            continue

    return datetime.today()


def get_date_range(months: int):
    """Calculates how many months of data you want to scrape
    Example 0 and 1 is a month until today, 2 is two months until today"""
    current_date = datetime.today()
    if months <= 0:
        return current_date
    else:
        return current_date - relativedelta(months=months)

# #Test cases
# dates = ["June 21, 2014", "Nov. 12, 2020", "Sep. 16, 2014", "Sept. 16, 2014", "1 hour ago"]
#
# # Convert and print dates
# for date in dates:
#     date_object = convert_to_date(date)
#     if date_object:
#         formatted_date = date_object.strftime("%Y-%m-%d")
#         print(f"Original: {date} -> Converted: {formatted_date}")
#     else:
#         print(f"Original: {date} -> Error: Unsupported date format")
