import tkinter as tk
from tkinter import messagebox
from Journal import Journal, Entry


class JournalGUI:
    def __init__(self, journal):
        self.journal = journal

        self.root = tk.Tk()
        self.root.title("My Journal")

        # Set custom background color and font
        self.root.configure(bg="#F2F2F2")
        self.root.option_add("*Font", "Arial 10")

        self.welcome_label = tk.Label(self.root, text="Welcome to My Journal!", bg="#F2F2F2", fg="#333333", font=("Arial", 16, "bold"))
        self.welcome_label.pack(pady=20)

        self.menu_frame = tk.Frame(self.root, bg="#F2F2F2")
        self.menu_frame.pack()

        self.new_entry_button = tk.Button(self.menu_frame, text="New Entry", command=self.open_new_entry_page, bg="#2196F3", fg="white",
                                          activebackground="#1976D2", activeforeground="white", font=("Arial", 12, "bold"))
        self.new_entry_button.pack(side=tk.LEFT, padx=10)

        self.search_entry_button = tk.Button(self.menu_frame, text="Search Entry", command=self.open_search_entry_page, bg="#4CAF50", fg="white",
                                             activebackground="#388E3C", activeforeground="white", font=("Arial", 12, "bold"))
        self.search_entry_button.pack(side=tk.LEFT, padx=10)

        self.other_functionality_button = tk.Button(self.menu_frame, text="Other Functionality", command=self.open_other_functionality_page,
                                                    bg="#F44336", fg="white", activebackground="#D32F2F", activeforeground="white",
                                                    font=("Arial", 12, "bold"))
        self.other_functionality_button.pack(side=tk.LEFT, padx=10)

    def open_new_entry_page(self):
        # Create a new window for writing a new entry
        new_entry_window = tk.Toplevel(self.root)
        new_entry_window.title("New Entry")

        # Set custom background color and font
        new_entry_window.configure(bg="#F2F2F2")
        new_entry_window.option_add("*Font", "Arial 10")

        entry_frame = tk.Frame(new_entry_window, bg="#F2F2F2")
        entry_frame.pack(pady=20)

        date_label = tk.Label(entry_frame, text="Date:", bg="#F2F2F2")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = tk.Entry(entry_frame, bg="white", fg="black", font=("Arial", 10))
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        title_label = tk.Label(entry_frame, text="Title:", bg="#F2F2F2")
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        title_entry = tk.Entry(entry_frame, bg="white", fg="black", font=("Arial", 10))
        title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        content_label = tk.Label(entry_frame, text="Content:", bg="#F2F2F2")
        content_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        content_entry = tk.Entry(entry_frame, bg="white")

        content_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        mood_label = tk.Label(entry_frame, text="Mood:", bg="#F2F2F2")
        mood_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        mood_entry = tk.Entry(entry_frame, bg="white", fg="black", font=("Arial", 10))
        mood_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        add_button = tk.Button(new_entry_window, text="Add Entry", command=lambda: self.add_entry(date_entry.get(), title_entry.get(), content_entry.get(), mood_entry.get()),
                               bg="#4CAF50", fg="white", activebackground="#45A049", activeforeground="white", font=("Arial", 10, "bold"))
        add_button.pack(pady=10)

    def add_entry(self, date, title, content, mood):
        if date and title and content and mood:
            entry = Entry(date, title, content, mood)
            self.journal.add_entry(entry)
            messagebox.showinfo("Entry Added", "Entry added successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled in.")

    def open_search_entry_page(self):
        # Create a new window for searching an entry
        search_entry_window = tk.Toplevel(self.root)
        search_entry_window.title("Search Entry")

        # Set custom background color and font
        search_entry_window.configure(bg="#F2F2F2")
        search_entry_window.option_add("*Font", "Arial 10")

        search_frame = tk.Frame(search_entry_window, bg="#F2F2F2")
        search_frame.pack(pady=20)

        date_label = tk.Label(search_frame, text="Search by Date:", bg="#F2F2F2")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = tk.Entry(search_frame, bg="white", fg="black", font=("Arial", 10))
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        title_label = tk.Label(search_frame, text="Search by Title:", bg="#F2F2F2")
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        title_entry = tk.Entry(search_frame, bg="white", fg="black", font=("Arial", 10))
        title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        search_button = tk.Button(search_entry_window, text="Search", command=lambda: self.search_entry(date_entry.get(), title_entry.get()),
                                  bg="#2196F3", fg="white", activebackground="#1976D2", activeforeground="white", font=("Arial", 10, "bold"))
        search_button.pack(pady=10)

    def search_entry(self, date, title):
        if date:
            entries = self.journal.search_entries_by_date(date)
        elif title:
            entries = self.journal.search_entries_by_title(title)
        else:
            entries = []

        if entries:
            messagebox.showinfo("Search Results", "Found {} entries.".format(len(entries)))
        else:
            messagebox.showinfo("Search Results", "No entries found.")

    def open_other_functionality_page(self):
        # Create a new window for other functionality
        other_functionality_window = tk.T
        other_functionality_window = tk.Toplevel(self.root)
        other_functionality_window.title("Other Functionality")

        # Set custom background color and font
        other_functionality_window.configure(bg="#F2F2F2")
        other_functionality_window.option_add("*Font", "Arial 10")

        # Add your other functionality components to the window

    def populate_entry_listbox(self):
        self.entry_listbox.delete(0, tk.END)
        entries = self.journal.get_entries()
        for entry in entries:
            self.entry_listbox.insert(tk.END, entry.get_summary())

    def on_entry_select(self, event):
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
        self.date_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.content_entry.delete(0, tk.END)
        self.mood_entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()


# Create a Journal object
journal = Journal()

# Create a JournalGUI object
app = JournalGUI(journal)

# Run the application
app.run()