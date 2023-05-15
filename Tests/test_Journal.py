import unittest
import datetime
from Entry import Entry
from Journal import Journal


class TestJournal(unittest.TestCase):
    
    
    def setUp(self):
        self.journal = Journal()

    
    def test_add_entry(self):
        date = datetime.date.today()
        title = "My day"
        mood = "happy"
        text = "Today was a great day!"
        entry = Entry(date, mood, title,text)
        self.journal.add_entry(entry)
        entries = self.journal.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_date(), date)
        self.assertEqual(entries[0].get_mood(), mood)
        self.assertEqual(entries[0].get_text(), text)
        self.assertEqual(entries[0].get_title(), title)

    
    def test_remove_entry(self):
        date = datetime.date.today()
        mood = "happy"
        title = "My day"
        text = "Today was a great day!"
        entry = Entry(date, mood, title, text)
        self.journal.add_entry(entry)
        self.journal.remove_entry(entry)
        entries = self.journal.get_entries()
        self.assertEqual(len(entries), 0)

    
    def test_get_entries(self):
        date1 = datetime.date.today()
        title1 = "My day"
        mood1 = "happy"
        text1 = "Today was a great day!"
        entry1 = Entry(date1, mood1, title1, text1)
        self.journal.add_entry(entry1)

        date2 = datetime.date.today() - datetime.timedelta(days=1)
        title2 = "My yesterday"
        mood2 = "sad"
        text2 = "Yesterday was a terrible day."
        entry2 = Entry(date2, mood2, title2, text2)
        self.journal.add_entry(entry2)

        entries = self.journal.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertIn(entry1, entries)
        self.assertIn(entry2, entries)

    
    def test_get_entry_by_date(self):
        date1 = datetime.date.today()
        mood1 = "happy"
        title1 = "My day"
        text1 = "Today was a great day!"
        entry1 = Entry(date1, mood1, title1,text1)
        self.journal.add_entry(entry1)

        date2 = datetime.date.today() - datetime.timedelta(days=1)
        mood2 = "sad"
        title2 = "My yesterday"
        text2 = "Yesterday was a terrible day."
        entry2 = Entry(date2, mood2, title2, text2)
        self.journal.add_entry(entry2)

        retrieved_entry = self.journal.get_entry_by_date(date1)
        self.assertEqual(retrieved_entry, entry1)

        retrieved_entry = self.journal.get_entry_by_date(date2)
        self.assertEqual(retrieved_entry, entry2)
        