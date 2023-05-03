import unittest
from datetime import date
from entry import Entry


class TestEntry(unittest.TestCase):

    
    def setUp(self):
        self.entry = Entry(date.today(), "happy", "Today was a great day!", "My Happy Day")

    
    def test_get_id(self):
        self.assertIsNone(self.entry.get_id())
        self.entry.set_id(1)
        self.assertEqual(self.entry.get_id(), 1)

    
    def test_get_date(self):
        self.assertEqual(self.entry.get_date(), date.today())

    
    def test_set_date(self):
        new_date = date(2023, 5, 3)
        self.entry.set_date(new_date)
        self.assertEqual(self.entry.get_date(), new_date)

    
    def test_get_mood(self):
        self.assertEqual(self.entry.get_mood(), "happy")

    
    def test_set_mood(self):
        self.entry.set_mood("sad")
        self.assertEqual(self.entry.get_mood(), "sad")

    
    def test_get_text(self):
        self.assertEqual(self.entry.get_text(), "Today was a great day!")

    
    def test_set_text(self):
        self.entry.set_text("Today was a terrible day!")
        self.assertEqual(self.entry.get_text(), "Today was a terrible day!")

        
