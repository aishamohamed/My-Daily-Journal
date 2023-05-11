import unittest
from User import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.hashed_password = User.hash_password(self.password)
        self.user = User(self.username, self.password)

    def test_hash_password(self):
        hashed_password = User.hash_password(self.password)
        self.assertEqual(hashed_password, self.hashed_password)

    def test_check_password(self):
        self.assertTrue(User.check_password(self.hashed_password, self.password))
        self.assertFalse(User.check_password(self.hashed_password, "wrongpassword"))

    def test_save_to_db(self):
        # Save the user to the database
        self.user.save_to_db()

        # Retrieve the user from the database
        retrieved_user = User.get_user_by_username(self.username)

        # Assert that the retrieved user has the same username and password
        self.assertEqual(retrieved_user.username, self.user.username)
        self.assertEqual(retrieved_user.password, self.user.password)

    def test_login(self):
        self.assertTrue(self.user.login(self.password))
        self.assertFalse(self.user.login("wrongpassword"))

if __name__ == '__main__':
    unittest.main()
