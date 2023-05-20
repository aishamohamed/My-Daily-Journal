import hashlib
import sqlite3
import os
from tempfile import NamedTemporaryFile
import unittest
from User import User

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
   

if __name__ == '__main__':
    unittest.main()
