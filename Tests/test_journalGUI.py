from multiprocessing.context import _default_context
from tkinter import messagebox, Tk
import tkinter as tk
import unittest
from JournalGUI import JournalGUI
from Journal import Journal, Entry, User
from datetime import datetime


class TestJournalGUI(unittest.TestCase):
    def setUp(self):
        """Set up the test case by creating a Journal and JournalGUI object."""
        self.journal = Journal()  # Instantiate Journal object
        self.app = JournalGUI(self.journal)  # Instantiate JournalGUI object
        self.root = Tk()
        self.app.root = self.root

    def test_login_successful(self):
        # Arrange
        username = "test_user"
        password = "test_password"
        self.journal.authenticate_user.return_value = User(username, password)

        # Act
        with unittest.mock.patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.gui.login(username, password)

        # Assert
        self.journal.authenticate_user.assert_called_with(username, password)
        mock_showinfo.assert_called_with("Login", "Login successful!")

    def test_login_failed(self):
        # Arrange
        username = "test_user"
        password = "test_password"
        self.journal.authenticate_user.return_value = None

        # Act
        with unittest.mock.patch('tkinter.messagebox.showerror') as mock_showerror:
            self.gui.login(username, password)

        # Assert
        self.journal.authenticate_user.assert_called_with(username, password)
        mock_showerror.assert_called_with("Login", "Invalid username or password.")
    
    def test_create_welcome_label(self):
        self.app.create_welcome_label()
        self.assertIsInstance(self.app.welcome_label, tk.Label)
        self.assertEqual(self.app.welcome_label.cget('text'), "Welcome to My Daily Journal!")
    
    def test_create_discription(self):
        self.app.create_discription()
        self.assertIsInstance(self.app.discription, tk.Label)
        self.assertIn("This app allows you to write and manage your personal journal entries!", self.app.discription.cget('text'))
    
    def test_create_menu_frame(self):
        self.app.create_menu_frame()
        self.assertIsInstance(self.app.menu_frame, tk.Frame)
    
    def test_create_new_entry_button(self):
        self.app.create_new_entry_button()
        self.assertIsInstance(self.app.new_entry_button, tk.Button)
        self.assertEqual(self.app.new_entry_button.cget('text'), "New Entry")
    
    def test_create_delete_button(self):
        self.app.create_delete_button()
        self.assertIsInstance(self.app.new_entry_button, tk.Button)
        self.assertEqual(self.app.new_entry_button.cget('text'), "Delete Entry")
    
    def test_create_search_entry_button(self):
        self.app.create_search_entry_button()
        self.assertIsInstance(self.app.search_entry_button, tk.Button)
        self.assertEqual(self.app.search_entry_button.cget('text'), "Search Entry")
    
    def test_create_display_all_entries_button(self):
        self.app.create_display_all_entries_button()
        self.assertIsInstance(self.app.other_functionality_button, tk.Button)
        self.assertEqual(self.app.other_functionality_button.cget('text'), "Display all entries")

    def test_open_new_entry_page(self):
        """Test the functionality of opening a new entry page."""
        self.app.open_new_entry_page()
        
        # Check if the new entry window is created and displayed
        self.assertIsInstance(self.app.new_entry_window, tk.Toplevel)
        self.assertEqual(self.app.new_entry_window.title(), "New Entry")

        # Check if the entry frame is present
        entry_frame = self.app.new_entry_window.nametowidget(".!toplevel.!frame.!frame")
        self.assertIsInstance(entry_frame, tk.Frame)

        # Check if the date label and entry field are present
        date_label = entry_frame.nametowidget(".!toplevel.!frame.!frame.!label")
        self.assertIsInstance(date_label, tk.Label)
        self.assertEqual(date_label["text"], "Date:")

        date_entry = entry_frame.nametowidget(".!toplevel.!frame.!frame.!entry")
        self.assertIsInstance(date_entry, tk.Entry)

        # Check if the title label and entry field are present
        title_label = entry_frame.nametowidget(".!toplevel.!frame.!frame.!label2")
        self.assertIsInstance(title_label, tk.Label)
        self.assertEqual(title_label["text"], "Title:")

        title_entry = entry_frame.nametowidget(".!toplevel.!frame.!frame.!entry2")
        self.assertIsInstance(title_entry, tk.Entry)

        # Check if the content label and text field are present
        content_label = entry_frame.nametowidget(".!toplevel.!frame.!frame.!label3")
        self.assertIsInstance(content_label, tk.Label)
        self.assertEqual(content_label["text"], "Content:")

        content_entry = entry_frame.nametowidget(".!toplevel.!frame.!frame.!text")
        self.assertIsInstance(content_entry, tk.Text)

        # Check if the mood label and entry field are present
        mood_label = entry_frame.nametowidget(".!toplevel.!frame.!frame.!label4")
        self.assertIsInstance(mood_label, tk.Label)
        self.assertEqual(mood_label["text"], "Mood:")

        mood_entry = entry_frame.nametowidget(".!toplevel.!frame.!frame.!entry3")
        self.assertIsInstance(mood_entry, tk.Entry)

        # Check if the add button is present
        add_button = self.app.new_entry_window.nametowidget(".!toplevel.!button")
        self.assertIsInstance(add_button, tk.Button)
        self.assertEqual(add_button["text"], "Add Entry")

    def test_add_entry(self):
        """Test adding an entry through the GUI."""
        self.app.open_new_entry_page()
        date_entry = self.app.date_entry
        title_entry = self.app.title_entry
        content_entry = self.app.content_entry
        mood_entry = self.app.mood_entry

        date_entry.insert(tk.END, "2023-05-05")
        title_entry.insert(tk.END, "My Entry")
        content_entry.insert(tk.END, "This is my entry content.")
        mood_entry.insert(tk.END, "Happy")

        self.app.add_entry()

        entries = self.journal.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_date(), "2023-05-05")
        self.assertEqual(entries[0].get_title(), "My Entry")
        self.assertEqual(entries[0].get_content(), "This is my entry content.")
        self.assertEqual(entries[0].get_mood(), "Happy")

        # Assert the message box is displayed with the success message
        self.assertEqual(self.root.children['!messagebox']['message'], "Entry added successfully!")

    def test_open_search_entry_page(self):
        """Test the functionality of opening the search entry page."""
        self.app.open_search_entry_page()

        # Assert the existence of the search entry window
        self.assertEqual(self.root.winfo_exists(), 1)
        self.assertEqual(self.root.winfo_name(), "Search Entry")

        # Assert the presence of required widgets in the search entry window
        date_label = self.root.children['!frame'].children['!label']
        self.assertEqual(date_label['text'], "Search by Date:")

        title_label = self.root.children['!frame'].children['!label2']
        self.assertEqual(title_label['text'], "Search by Title:")

        search_button = self.root.children['!button']
        self.assertEqual(search_button['text'], "Search")

    def test_search_entry_no_results(self):
        """Ensure the search entry functionality works correctly when no results are found"""
        date = datetime.now().strftime("%Y-%m-%d")
        title = "Test Entry"
        content = "This is a test entry."
        mood = "Happy"

        entry = Entry(date, title, content, mood)
        self.journal.add_entry(entry)

        # Trigger the search entry functionality with invalid search criteria
        self.app.search_entry("2023-01-01", "Invalid Title")

        # Assert the message box is displayed with the no results message
        messagebox = self.root.children['!messagebox']
        self.assertEqual(messagebox['message'], "No entries found.")
    
    def test_search_entry_with_results(self):
        """Ensure the search entry functionality works correctly when results are found"""
        date = datetime.now().strftime("%Y-%m-%d")
        title = "Test Entry"
        content = "This is a test entry."
        mood = "Happy"

        entry = Entry(date, title, content, mood)
        self.journal.add_entry(entry)

        # Trigger the search entry functionality with valid search criteria
        self.app.search_entry(date, title)

        # Assert the message box is displayed with the search results
        messagebox = self.root.children['!messagebox']
        self.assertEqual(messagebox['message'], "Search Results:\n\nDate: {}\nTitle: {}\nMood: {}\nContent:\n{}\n\n".format(date, title, mood, content))


    def test_display_search_results(self):
        """Test displaying the search results in a message box."""
        entries = [
            Entry("2023-05-05", "Happy", "My Entry", "This is my entry content.")
        ]
        self.app.display_search_results(entries)
    def test_populate_entry_listbox(self):
        """Ensure the entry listbox is properly populated with entries"""
        date = datetime.now().strftime("%Y-%m-%d")
        title = "Test Entry"
        content = "This is a test entry."
        mood = "Happy"

        entry = Entry(date, title, content, mood)
        self.journal.add_entry(entry)

        self.app.populate_entry_listbox()

        # Assert the entry listbox is populated with the entry summary
        listbox = self.root.children['!listbox']
        self.assertEqual(listbox.size(), 1)
        self.assertEqual(listbox.get(0), "Test Entry - {}".format(date))
    
    def test_on_entry_select(self):
        """Ensure the entry details are properly displayed when an entry is selected"""
        date = datetime.now().strftime("%Y-%m-%d")
        title = "Test Entry"
        content = "This is a test entry."
        mood = "Happy"

        entry = Entry(date, title, content, mood)
        self.journal.add_entry(entry)

        self.app.populate_entry_listbox()

        # Trigger the entry selection
        listbox = self.root.children['!listbox']
        listbox.selection_set(0)
        self.app.on_entry_select(None)

        # Assert the entry details are displayed correctly
        date_entry = self.root.children['!frame'].children['!entry']
        self.assertEqual(date_entry.get(), date)

        title_entry = self.root.children['!frame'].children['!entry2']
        self.assertEqual(title_entry.get(), title)

        content_entry = self.root.children['!frame'].children['!text']
        self.assertEqual(content_entry.get(1.0, tk.END), content)
        mood_entry = self.root.children['!frame'].children['!entry6']
        self.assertEqual(mood_entry.get(), mood)
    
    def test_run(self):
        """ Ensure the GUI application runs without errors"""
        self.app.run()

        # Assert the main application loop is running
        self.assertEqual(self.root.tk.call("info", "exists", "."), "1")

    def tearDown(self):
        """Clean up after each test by destroying the root window."""
        self.app.root.destroy()
        self.root.destroy()
        _default_context.destroy()

if __name__ == '__main__':
    unittest.main()