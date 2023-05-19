import hashlib
import sqlite3
import os
from tempfile import NamedTemporaryFile
from user import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.db_file = NamedTemporaryFile(delete=False)
        self.db_filename = self.db_file.name
        self.conn = sqlite3.connect(self.db_filename)
        self.create_table()

    def tearDown(self):
        # Close the database connection and delete the temporary file
        self.conn.close()
        os.unlink(self.db_filename)

    def create_table(self):
        # Create a 'users' table in the temporary database for testing
        with self.conn:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            password TEXT
                         )''')

    def test_save_to_db(self):
        # Create a new user object and save it to the database
        user = User("testuser", "testpassword")
        user.save_to_db()

        # Retrieve the user from the database
        with self.conn:
            c = self.conn.cursor()
            c.execute('SELECT * FROM users WHERE username=?', ("testuser",))
            row = c.fetchone()
            self.assertIsNotNone(row)
            id, username, password = row
            self.assertEqual(username, "testuser")
            self.assertTrue(User.check_password(password, "testpassword"))

    def test_get_user_by_username(self):
        # Create a new user object and save it to the database
        user = User("testuser", "testpassword")
        user.save_to_db()

        # Retrieve the user from the database using the get_user_by_username method
        retrieved_user = User.get_user_by_username("testuser")

        # Check if the retrieved user is not None and has the correct attributes
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertTrue(User.check_password(retrieved_user.password, "testpassword"))

    def test_login(self):
        # Create a new user object and save it to the database
        user = User("testuser", "testpassword")
        user.save_to_db()

        # Attempt to log in with the correct password
        self.assertTrue(user.login("testpassword"))

        # Attempt to log in with an incorrect password
        self.assertFalse(user.login("incorrectpassword"))




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
   

if __name__ == '__main__':
    unittest.main()
