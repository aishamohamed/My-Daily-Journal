import datetime
import sqlite3
from Entry import Entry


class Journal:
    """Class to represent a journal and manage entries."""

    def __init__(self):
        """
        Initialize a journal object and create the entries table in the database if it does not exist.
        """
        self.conn = sqlite3.connect('journal.db')
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE IF EXISTS entries")  # Drop the existing table if it exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS entries
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             date TEXT,
                             mood TEXT,
                             title TEXT,
                             text TEXT)''')
        self.conn.commit()

    def add_entry(self, entry):
        """
        Add an entry to the database.

        :param entry: The entry to add.
        :type entry: Entry
        """
        self.c.execute("INSERT INTO entries (date, mood, title, text) VALUES (?, ?, ?, ?)",
                       (entry.get_date().strftime("%Y-%m-%d %H:%M:%S"), entry.get_mood(), entry.get_title(),entry.get_text()))
        self.conn.commit()

    def remove_entry(self, entry):
        """Removes an entry from the SQLite database.

        Args:
            Entry: The Entry object to remove from the database.

        """
        self.c.execute("DELETE FROM entries WHERE id = ?", (entry.get_id(),))
        self.conn.commit()
    
    def get_entries(self):
        """Retrieves a list of all entries from the SQLite database.

        Returns:
            list: A list of Entry objects.

        """
        self.c.execute("PRAGMA table_info(entries)")
        rows = self.c.fetchall()
        entries = []
        try:
            for row in rows:
                entry = Entry(row[1], row[2], row[3], row[4], row[0])
                entries.append(entry)
            return entries
        except ValueError:
            print(f"Invalid date value in entry with ID {row[0]}. Skipping entry.")
        return entries

    def get_entry_by_id(self, entry_id):
        """Get an entry from the database by its ID.

        Args:
            entry_id (int): The ID of the entry to retrieve.

        Returns:
            Entry: The retrieved entry, or None if not found.
        """
        self.c.execute("SELECT * FROM entries WHERE id = ?", (entry_id,))
        row = self.c.fetchone()
        if row:
            entry = Entry(row[1], row[2], row[3], row[4],row[0])
            return entry
        else:
            return None

    def get_entry_by_date(self, date):
        """Get an entry from the database by its date.

        Args:
            date (datetime.date): The date of the entry to retrieve.

        Returns:
            Entry: The retrieved entry, or None if not found.
        """
        self.c.execute("SELECT * FROM entries WHERE date = ?", (str(date),))
        row = self.c.fetchone()
        if row is None:
            return None
        entry = Entry(row[1], row[2], row[3], row[4])
        entry.set_id(row[0])
        return entry
    
    def get_entry_by_title(self, title):
        """Searches entries in the database by title.

        Args:
            title (str): The title to search for.

        Returns:
            list: A list of Entry objects matching the search criteria.
        """
        self.c.execute("SELECT * FROM entries WHERE title LIKE ?", ('%' + title + '%',))
        rows = self.c.fetchall()
        entries = []
        for row in rows:
            entry = Entry(row[1], row[2], row[3], row[4], row[0])
            entries.append(entry)
        return entries