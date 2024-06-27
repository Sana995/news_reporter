class Article:
    """
    A class to represent a news article.

    Attributes:
    -----------
    title : str
        The title of the news article.
    description : str
        A brief description of the news article.
    date : str
        The publication date of the news article.
    file_path : str
        The file path where the article is stored.
    flag_amount : int
        The amount of flags associated with the news article.
    no_of_keywords : int
        The number of keywords associated with the news article.
    """
    def __init__(self, title, description, date, file_path, flag_amount, no_of_keywords):
        self.title = title
        self.description = description
        self.date = date
        self.file_path = file_path
        self.flag_amount = flag_amount
        self.no_of_keywords = no_of_keywords

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Date: {self.date}\n"
            f"File Path: {self.file_path}\n"
            f"Flag Amount: {self.flag_amount}\n"
            f"Number of Keywords: {self.no_of_keywords}"
        )
