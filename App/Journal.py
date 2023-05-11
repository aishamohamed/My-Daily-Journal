import datetime
import sqlite3
from Entry import Entry
from User import User 


class Journal:
    """Class to represent a journal and manage entries."""

    def __init__(self):
        """
        Initialize a journal object and create the entries table in the database if it does not exist.
        """
        self.conn = sqlite3.connect('journal.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS entries
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             date TEXT,
                             mood TEXT,
                             title TEXT,
                             text TEXT,
                             user_id INTEGER,
                             FOREIGN KEY(user_id) REFERENCES users(id))''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             username TEXT UNIQUE,
                             password TEXT)''')
        self.conn.commit()
    
    def close(self):
        self.conn.close()

    def add_user(self, username, password):
        """
        Add a user to the database.

        :param username: The username of the user to add.
        :type username: str
        :param password: The password of the user to add.
        :type password: str
        """
        user = User(username, password)
        try: 
            self.c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        (user.username, user.password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Username {username} already exists. Please choose a different username.")
            return False

    def authenticate_user(self, username, password):
        """
        Authenticate a user.

        :param username: The username of the user to authenticate.
        :type username: str
        :param password: The password of the user to authenticate.
        :type password: str
        :return: The user ID if authentication is successful, None otherwise.
        :rtype: int or None
        """
        self.c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        row = self.c.fetchone()
        if row and User.check_password(row[2], password):
            return User(row[1], row[2], row[0])
        else:
            return None

    def add_entry(self, entry, user):
        """
        Add an entry to the database.

        :param entry: The entry to add.
        :type entry: Entry
        :param user: The user who created the entry.
        :type user: User
        """
        with self.conn:
            self.c.execute("INSERT INTO entries (date, mood, title, text, user_id) VALUES (?, ?, ?, ?, ?)",
                        (entry.get_date().strftime("%Y-%m-%d %H:%M:%S"), entry.get_mood(), entry.get_title(),entry.get_text(), user.id))

    def remove_entry(self, entry):
        """Removes an entry from the SQLite database.

        Args:
            Entry: The Entry object to remove from the database.

        """
        self.c.execute("DELETE FROM entries WHERE id = ?", (entry.get_id(),))
        self.conn.commit()
    
    def get_entries(self, user):
        """Retrieves a list of all entries for the given user from the SQLite database.

        Returns:
            list: A list of Entry objects.

        """
        self.c.execute("SELECT * FROM entries WHERE user_id = ?", (user.id,))
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

    def get_entry_by_id(self, entry_id, user):
        """Get an entry from the database by its ID.

        Args:
            entry_id (int): The ID of the entry to retrieve.
            user (User): The user who created the entry.
        Returns:
            Entry: The retrieved entry, or None if not found.
        """
        self.c.execute("SELECT * FROM entries WHERE id = ? AND user_id = ?", (entry_id, user.id))
        row = self.c.fetchone()
        if row:
            entry = Entry(row[1], row[2], row[3], row[4],row[0])
            return entry
        else:
            return None

    def get_entry_by_date(self, date, user):
        """Get an entry from the database by its date.

        Args:
            date (datetime.date): The date of the entry to retrieve.
            user (User): The user who created the entry.
        Returns:
            list: A list of retrieved entries, or an empty list if none are found.
        """
        date_str_start = date.strftime("%Y-%m-%d 00:00:00")
        date_str_end = date.strftime("%Y-%m-%d 23:59:59")
        self.c.execute("SELECT * FROM entries WHERE date >= ? AND date <= ? AND user_id = ?", 
                   (date_str_start, date_str_end, user.id))
        
        entries = []
        while True:
            row = self.c.fetchone()
            if row is None:
                break
            
            entry = Entry(row[1], row[2], row[3], row[4])
            entry.set_id(row[0])
            entries.append(entry)
        return entries