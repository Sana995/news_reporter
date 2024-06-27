import re


def find_keyword_matches(search_word, text):
    """Search text for a search word (case-insensitive), count how many times will it occur"""
    pattern = re.compile(re.escape(search_word), re.IGNORECASE)
    matches = pattern.findall(text)
    count = len(matches)
    return count


def contains_usd_amount(text):
    """This will check the text for USD amount and return True if present
    It will cover this formats: $11.1 | $111,111.11 | 11 dollars | 11 USD"""
    regex = r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|\b\d+(\.\d{1,2})?(,\d{3})* ?(dollars|USD)\b'
    # Search the text for the pattern
    if re.search(regex, text):
        return True
    else:
        return False

