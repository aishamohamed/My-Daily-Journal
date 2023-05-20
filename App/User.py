
import hashlib
import sqlite3


class User:
    """Class to represent a user."""

    def __init__(self, username, password, id=None):
        """
        Initialize a user object.

        :param username: The username of the user.
        :type username: str
        :param password: The password of the user.
        :type password: str
        :param id: The ID of the user (optional).
        :type id: int or None
        """
        self.username = username
        self.password = User.hash_password(password)
        self.id = id

    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA256.

        :param password: The password to hash.
        :type password: str
        :return: The hashed password.
        :rtype: str
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(hashed_password, password):
        """
        Check if a password matches its hashed value.

        :param hashed_password: The hashed password to check.
        :type hashed_password: str
        :param password: The password to compare.
        :type password: str
        :return: True if the password matches, False otherwise.
        :rtype: bool
        """
        return hashed_password == User.hash_password(password)

    def save_to_db(self):
        """
        Save the user object to the database.
        """
        with sqlite3.connect('journal.db') as conn:
            c = conn.cursor()
            if self.id is None:
                # Insert a new row
                c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                          (self.username, self.password))
                self.id = c.lastrowid
            else:
                # Update an existing row
                c.execute('UPDATE users SET username=?, password=? WHERE id=?',
                          (self.username, self.password, self.id))
    @staticmethod
    def get_user_by_username(username):
        """
        Retrieve a user object by username from the database.

        :param username: The username of the user to retrieve.
        :type username: str
        :return: The user object.
        :rtype: User or None
        """
        with sqlite3.connect('journal.db') as conn:
            c = conn.cursor()
            c.execute('SELECT id, password FROM users WHERE username=?', (username,))
            row = c.fetchone()
            if row is not None:
                id, password = row
                return User(username, password, id=id)

    def login(self, password):
        """
        Attempt to log in with a password.

        :param password: The password to use for authentication.
        :type password: str
        :return: True if the login is successful, False otherwise.
        :rtype: bool
        """
        return User.check_password(self.password, password)