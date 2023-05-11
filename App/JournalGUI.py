from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox
from Journal import Journal, Entry, User


class JournalGUI:
    """
    Graphical User Interface for the Journal application.
    """
    def __init__(self, journal):
        """
        Initialize the JournalGUI.

        Args:
            journal (Journal): The Journal object to interact with.
        """
        self.journal = journal
        self.user = User
        self.current_user = None 

        # Define colors
        self.color1 = "#FFFFFF"  # White
        self.color2 = "#2E8B57"  # Sea Green
        self.color3 = "#006400"  # Sea Green 4
        self.color4 = "#20B2AA"  # Sea Green 3

        self.open_login_page()


    def start(self):
        
        self.root = tk.Tk()
        self.root.title("My Journal")

        # Set custom background color and font
        self.root.configure(bg=self.color4)
        self.root.option_add("*Font", "Arial 10")

        # Adjust the window geometry
        window_width = 800  # Set your desired width
        window_height = 600  # Set your desired height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.create_welcome_label()
        self.create_menu_frame()
        self.create_new_entry_button()
        self.create_search_entry_button()
        self.create_display_all_entries_button()

    def create_welcome_label(self):
        self.welcome_label = tk.Label(self.root, text="Welcome to My Journal!", bg=self.color4, fg="#333333", font=("Arial", 16, "bold"))
        self.welcome_label.pack(pady=20, anchor=tk.CENTER)

    def create_menu_frame(self):
        self.menu_frame = tk.Frame(self.root, bg=self.color4)
        self.menu_frame.pack()

    def create_new_entry_button(self):
        self.new_entry_button = tk.Button(self.menu_frame, text="New Entry", command=self.open_new_entry_page, bg="#2E8B57", fg="white",
                                          activebackground="#1976D2", activeforeground="white", font=("Arial", 12, "bold"))
        self.new_entry_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    def create_search_entry_button(self):
        self.search_entry_button = tk.Button(self.menu_frame, text="Search Entry", command=self.open_search_entry_page, bg="#4CAF50", fg="white",
                                             activebackground="#388E3C", activeforeground="white", font=("Arial", 12, "bold"))
        self.search_entry_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    def create_display_all_entries_button(self):
        self.other_functionality_button = tk.Button(self.menu_frame, text="Display all entries", command=self.display_all_entries,
                                                    bg="#2E2E8B", fg="white", activebackground="#2E2E8B", activeforeground="white",
                                                    font=("Arial", 12, "bold"))
        self.other_functionality_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    def open_login_page(self):
        """
        Open a new window for logging in to the journal.
        """
        login_window = self.root = tk.Tk()
        login_window.title("Login")
        

        # Adjust the window geometry
        window_width = 270  # Set your desired width
        window_height = 200  # Set your desired height
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Set custom background color and font
        login_window.configure(bg=self.color4)
        login_window.option_add("*Font", "Arial 10")

        # create the login frame
        login_frame = tk.Frame(login_window, bg=self.color4)
        login_frame.grid(row=0, column=0, padx=20, pady=10)

        # create the login labels and entries
        login_label = tk.Label(login_window, text="Please log in:", bg= self.color4)
        login_label.grid(row=1, column=0, columnspan=2)

        username_label = tk.Label(login_frame, text="Username:", bg=self.color4)
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        username_entry = tk.Entry(login_frame, bg="white", fg="black", font=("Arial", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        password_label = tk.Label(login_frame, text="Password:", bg=self.color4)
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        password_entry = tk.Entry(login_frame, bg="white", fg="black", font=("Arial", 10), show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # create the login button
        login_button = tk.Button(login_window, text="Log In", command=lambda: self.login(username_entry.get(), password_entry.get()),
                                  bg="#2E8B57", fg="white", activebackground="#1976D2", activeforeground="white", font=("Arial", 10, "bold"))
        login_button.grid(row=2, column=0)

        # create create account button
        create_account_button = tk.Button(login_window, text="Create account", command=self.create_user_screen,bg="#2E8B57", fg="white", font=("Arial", 10, "bold"))
        create_account_button.grid(row=3, column=0, padx=10,pady=10)
        

    def login(self, username, password):
        """Attempt to login with the provided username and password."""
        

        if username and password:
            user = self.journal.authenticate_user(username, password)
            if user is not None:
                self.current_user = user
                messagebox.showinfo("Login", "Login successful!")
                self.root.destroy()
                self.start()
                
            else:
                messagebox.showerror("Login", "Invalid username or password.")
        else:
            messagebox.showerror("Login", "Please enter a valid username and password.")
    
    def create_user_screen(self):
        """Create a user registration screen."""
        user_screen = tk.Toplevel(self.root)
        user_screen.title("User Registration")
        user_screen.geometry("300x200")

        user_screen.configure(bg="#F2F2F2")
        user_screen.option_add("*Font", "Arial 10")

        username_label = tk.Label(user_screen, text="Username:", bg="#F2F2F2")
        username_label.pack(pady=5)
        username_entry = tk.Entry(user_screen, bg="white", fg="black", font=("Arial", 10))
        username_entry.pack(pady=5)

        password_label = tk.Label(user_screen, text="Password:", bg="#F2F2F2")
        password_label.pack(pady=5)
        password_entry = tk.Entry(user_screen, show="*", bg="white", fg="black", font=("Arial", 10))
        password_entry.pack(pady=5)

        register_button = tk.Button(user_screen, text="Register", command=lambda: self.register_user(username_entry.get(), password_entry.get()),
                                  bg="#2196F3", fg="white", activebackground="#1976D2", activeforeground="white", font=("Arial", 10, "bold"))
        register_button.pack(pady=10)

        # create the cancel button
        cancel_button = tk.Button(user_screen, text="Cancel", command=user_screen.destroy)
        cancel_button.pack()

    def register_user(self, username, password):
        """Register a new user."""
        if username and password:
            if self.journal.add_user(username, password):
                messagebox.showinfo("User Registration", "User registration successful.")
            else:
                messagebox.showerror("User Registration", "Username already exists. Please choose a different username.")
        else:
            messagebox.showerror("User Registration", "Please enter a valid username and password.")

    def open_new_entry_page(self):
        """
        Open a new window for writing a new journal entry.
        """
        new_entry_window = tk.Toplevel(self.root)
        new_entry_window.title("New Entry")

        # Adjust the window geometry
        window_width = 800  # Set your desired width
        window_height = 600  # Set your desired height
        screen_width = new_entry_window.winfo_screenwidth()
        screen_height = new_entry_window.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        new_entry_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Set custom background color and font
        new_entry_window.configure(bg=self.color4)
        new_entry_window.option_add("*Font", "Arial 10")

        entry_frame = tk.Frame(new_entry_window, bg=self.color4)
        entry_frame.pack(pady=20)

        date_label = tk.Label(entry_frame, text="Date/Time:", bg=self.color4, fg="#000000")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = tk.Entry(entry_frame, bg=self.color1, fg=self.color2, font=("Arial", 12, "bold"))
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        # Populate date entry field with current date
        date_entry.insert(tk.END, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        title_label = tk.Label(entry_frame, text="Title:", bg=self.color4, fg="black")
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        title_entry = tk.Entry(entry_frame, bg=self.color1, fg="black", font=("Arial", 12, "bold"), width=40)
        title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        content_label = tk.Label(entry_frame, text="Content:", bg=self.color4, fg="black")
        content_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        content_entry = tk.Text(entry_frame, bg=self.color1, fg="black", font=("Arial", 11), height=20, width=60)
        content_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        mood_label = tk.Label(entry_frame, text="Mood:", bg=self.color4, fg="black")
        mood_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        mood_entry = tk.Entry(entry_frame, bg=self.color1, fg="black", font=("Arial", 11, "bold"), width=45)
        mood_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        add_button = tk.Button(new_entry_window, text="Save Entry", command=lambda: self.add_entry(new_entry_window,date_entry.get(), title_entry.get(), content_entry.get("1.0", tk.END), mood_entry.get()),
                               bg="#4CAF50", fg="white", activebackground="#45A049", activeforeground="white", font=("Arial", 10, "bold"))
        add_button.pack(pady=10)

    def add_entry(self, open_new_entry_page, date, title, content, mood):
        """
        Add a new entry to the journal.

        Args:
            new_entry_window (tk.Toplevel): The new entry window.
            date (str): The date of the entry.
            title (str): The title of the entry.
            content (str): The content of the entry.
            mood (str): The mood of the entry.
        """
        if date and title and content and mood:
            entry = Entry(date, title, content, mood)
            self.journal.add_entry(entry, self.current_user)
            print(self.journal.get_entries(self.current_user))
            messagebox.showinfo("Entry saved", "Entry saved successfully!")
            open_new_entry_page.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled in.")

    def open_search_entry_page(self):
        """Open a new window for searching a journal entry."""
        search_entry_window = tk.Toplevel(self.root)
        search_entry_window.title("Search Entry")

        # Adjust the window geometry
        window_width = 600  # Set your desired width
        window_height = 400  # Set your desired height
        screen_width = search_entry_window.winfo_screenwidth()
        screen_height = search_entry_window.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        search_entry_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Set custom background color and font
        search_entry_window.configure(bg=self.color4)
        search_entry_window.option_add("*Font", "Arial 10")

        search_frame = tk.Frame(search_entry_window, bg=self.color4)
        search_frame.pack(pady=20)

        date_label = tk.Label(search_frame, text="Search by Date:", bg=self.color4, font=("Arial", 11, "bold"))
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = tk.Entry(search_frame, bg="white", fg="black", font=("Arial", 10, "bold"))
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        date_message = tk.Label(search_frame, text="please use this format: YYYY-MM-DD", bg= self.color4, font=("Arial", 11, "bold"))
        date_message.grid(row=1, column=2, padx=5, pady=5)

        title_label = tk.Label(search_frame, text="Search by Title:", bg="#F2F2F2")
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        title_entry = tk.Entry(search_frame, bg="white", fg="black", font=("Arial", 10, "bold"))
        title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        search_button = tk.Button(search_entry_window, text="Search", command=lambda: self.search_entry(date_entry.get() if date_entry.get() else None, title_entry.get() if title_entry.get() else None), bg="#4CAF50", fg="white", activebackground="#45A049", activeforeground="white", font=("Arial", 10, "bold"))

        search_button.pack(pady=10)


    def search_entry(self, date, title):
        """
        Search for entries based on the specified date or title.

        Args:
            date (str): The date to search for in the format 'YYYY-MM-DD'.
            title (str): The title to search for.

        Returns:
            list: A list of Entry objects representing the search results.
        """
        self.journal.get_entries(self.current_user)
        entries = []

        if date and title:
            messagebox.showerror("Error", "Please search by either date or title, not both.")
            return

        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            entries = self.journal.get_entry_by_date(date_obj, self.current_user)
        elif title:
            title = ' '.join(title.split())
            entries = self.journal.get_entry_by_title(title.strip(), self.current_user)
        else:
            entries = []

        if entries:
            self.display_search_results(entries)
        else:
            messagebox.showinfo("Search Results", "No entries found.")


    def display_search_results(self, entries):
        """
        Display the search results in a message box.

        Args:
            entries (list): A list of Entry objects representing the search results.
         """
        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("Search Results")

        results_text = tk.Text(search_results_window, wrap=tk.WORD)
        results_text.pack(expand=True, fill=tk.BOTH)

        for entry in entries:
            results_text.insert(tk.END, f"Title: {entry.get_title()}\n")
            results_text.insert(tk.END, f"Date: {entry.get_date().strftime('%Y-%m-%d %H:%M:%S')}\n")
            results_text.insert(tk.END, f"Mood: {entry.get_mood()}\n")
            results_text.insert(tk.END, f"Content:\n{entry.get_text()}\n")
            results_text.insert(tk.END, "-" * 40 + "\n")


    def display_all_entries(self):
        """Open a new window for other functionality."""
        display_all_entries = tk.Toplevel(self.root)
        display_all_entries.title("Other Functionality")

        # Set custom background color and font
        display_all_entries.configure(bg=self.color3)  # Sea Green 4
        display_all_entries.option_add("*Font", "Arial 10")

        entry_listbox = tk.Listbox(display_all_entries, bg=self.color1, fg=self.color2, font=("Arial", 10), width=60, height=20)  # White background, Sea Green text
        entry_listbox.pack(padx=20, pady=20)

        entries = self.journal.get_entries(self.current_user)  # Fetch entries for current user
        for entry in entries:
            entry_summary = f"Tilte: {entry.get_mood()} - {entry.get_date()}. Mood: {entry.get_text()}"
            entry_listbox.insert(tk.END, entry_summary)


    def populate_entry_listbox(self):
        """
        Populate the entry listbox with entries from the journal.
        """
        self.entry_listbox.delete(0, tk.END)
        entries = self.journal.get_entries()
        for entry in entries:
            self.entry_listbox.insert(tk.END, entry.get_summary())


    def on_entry_select(self, event):
        """
        Handle the selection of an entry in the listbox.

        Args:
            event: The event object.
        """
        selected_index = self.entry_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            entry = self.journal.get_entry_by_index(selected_index)
            if entry:
                self.date_entry.delete(0, tk.END)
                self.title_entry.delete(0, tk.END)
                self.content_entry.delete(0, tk.END)
                self.mood_entry.delete(0, tk.END)

                self.date_entry.insert(tk.END, entry.get_date())
                self.title_entry.insert(tk.END, entry.get_title())
                self.content_entry.insert(tk.END, entry.get_content())
                self.mood_entry.insert(tk.END, entry.get_mood())

                self.detail_text.delete("1.0", tk.END)
                self.detail_text.insert(tk.END, entry.get_content())  # Display full content in detail text area


    def clear_entry_fields(self):
        """Clear the entry fields in the new entry page."""
        self.date_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.content_entry.delete(0, tk.END)
        self.mood_entry.delete(0, tk.END)


    def run(self):
        """Run the Journal GUI application."""
        self.root.mainloop()


# Create a Journal object
journal = Journal()

# Create a JournalGUI object
app = JournalGUI(journal)

# Run the application
app.run()
journal.close()