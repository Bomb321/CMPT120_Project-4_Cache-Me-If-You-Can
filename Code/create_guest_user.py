# Admin Create Guest User
# Simple Program to Create a Guest User within a Warehouse Management System
# Jack Teller

import tkinter as tk
from tkinter import messagebox

# User database
user_database = {}

def create_guest_user():
    # Get inputs from entry fields
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        return

    if username in user_database:
        messagebox.showerror("Error", "Username previously used, please try again.")
    else:
        user_database[username] = password
        messagebox.showinfo("Success", "New Guest User Successfully Created!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

# Initialize the main window
root = tk.Tk()
root.title("Guest User Creation")

# Create and place widgets
tk.Label(root, text="Enter a Username:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Enter a Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*", width=30)
password_entry.grid(row=1, column=1, padx=10, pady=5)

create_button = tk.Button(root, text="Create Guest User", command=create_guest_user)
create_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()




