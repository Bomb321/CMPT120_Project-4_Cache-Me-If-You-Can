# Admin Create Guest User
# Simple Program to Create a Guest User within a Warehouse Management System
# Jack Teller

import tkinter as tk
from tkinter import messagebox
import csv
import datetime

# Path to the CSV file
CSV_Guest = "guest_users.csv"

# Load user data from the CSV file
def load_users_from_csv():
    try:
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Ensures rows have both username and password
                    user_database[row[0]] = row[1]
    except FileNotFoundError:
        with open(CSV_FILE, mode="w") as file:  # Creates the file if it doesn't exist
            pass

# Save user data to the CSV file
def save_user_to_csv(username, password):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

# User database (in-memory dictionary for session use)
user_database = {}
load_users_from_csv()  # Load data on program start

def create_guest_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        return

    if username in user_database:
        messagebox.showerror("Error", "Username previously used, please try again.")
    else:
        user_database[username] = password
        save_user_to_csv(username, password)
        messagebox.showinfo("Success", "New Guest User Successfully Created!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

def display_user_count():
    user_count = len(user_database)
    messagebox.showinfo("User Count", f"There are currently {user_count} guest users.")

def display_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    messagebox.showinfo("Current Date", f"Today's date is: {current_date}")

def main_menu():
    messagebox.showinfo("Main Menu", "Main menu functionality will be implemented here.")
    root.destroy()

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

user_count_button = tk.Button(root, text="Show User Count", command=display_user_count)
user_count_button.grid(row=3, column=0, columnspan=2, pady=10)

date_button = tk.Button(root, text="Show Current Date", command=display_date)
date_button.grid(row=4, column=0, columnspan=2, pady=10)

main_menu_button = tk.Button(root, text="Main Menu", command=main_menu)
main_menu_button.grid(row=5, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()
