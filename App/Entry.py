from datetime import datetime

class Entry:
    """Represents a journal entry.

    Attributes:
        title (str): The title of the journal entry.
        date (datetime.date): The date of the journal entry.
        mood (str): The mood of the journal entry.
        text (str): The text content of the journal entry.
        id (int): The ID of the journal entry.
    """
    def __init__(self, date, mood, text, title, id=None):
        """Initializes an instance of Entry.

        Args:
            title (str): The title of the journal entry.
            date (datetime.date): The date of the journal entry.
            mood (str): The mood of the journal entry.
            text (str): The text content of the journal entry.
            id (int, optional): The ID of the journal entry. Defaults to None.
        """
        self.date = date
        self.mood = mood
        self.title = title
        self.text = text
        self.id = id


    def get_id(self):
        """
        Get the ID of the entry.

        :return: The ID of the entry.
        :rtype: int
        """
        return self.id

    def set_id(self, entry_id):
        """
        Set the ID of the entry.

        :param entry_id: The ID to set.
        :type entry_id: int
        """
        self._id = entry_id

    def get_date(self):
        """Returns the date of the journal entry.

        Returns:
            datetime.date: The date of the journal entry.
        """
        return datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")

    def set_date(self, date):
        """Sets the date of the journal entry.

        Args:
            date (datetime.date): The new date of the journal entry.
        """
        self.date = date
    def set_title(self, title):
        """Sets the title of the journal entry.

        Args:
            title (str): The new mood of the journal entry.
        """
        self.title = title
    
    def get_title(self):
        """Returns the title of the journal entry.

        Returns:
            str: The mood of the journal entry.
        """
        return self.title

    def get_mood(self):
        """Returns the mood of the journal entry.

        Returns:
            str: The mood of the journal entry.
        """
        return self.mood

    def set_mood(self, mood):
        """Sets the mood of the journal entry.

        Args:
            mood (str): The new mood of the journal entry.
        """
        self.mood = mood

    def get_text(self):
        """Returns the text content of the journal entry.

        Returns:
            str: The text content of the journal entry.
        """
        return self.text

    def set_text(self, text):
        """Sets the text content of the journal entry.

        Args:
            text (str): The new text content of the journal entry.
        """
        self.text = text