import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

# File names for storing user data and removed user logs
USER_DATA_FILE = 'user_data.csv'
REMOVED_USERS_FILE = 'removed_users_log.csv'

# Load user data from the CSV file
def userdata():
    if not os.path.exists(USER_DATA_FILE):
        return [], [], []  # returns empty lists if the file does not exist

    usernames, passwords, roles = [], [], []
    with open(USER_DATA_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # makes sure the row is not empty
                usernames.append(row[0])
                passwords.append(row[1])
                roles.append(row[2])
    return usernames, passwords, roles

# Save user data to the CSV file
def savedata():
    with open(USER_DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(usernames)):
            writer.writerow([usernames[i], userpasswords[i], userroles[i]])

# Log removed user data
def logremoved(username):
    with open(REMOVED_USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the username and the timestamp of removal
        writer.writerow([username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

usernames, userpasswords, userroles = userdata()

def message(msg):
    messagebox.showinfo("Information", msg)

def confirmremove(username_to_remove, num):
    confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove user '{username_to_remove}'?")
    if confirm:
        logremoved(username_to_remove)
        
        usernames.pop(num)
        userroles.pop(num)
        userpasswords.pop(num)
        savedata()  # Save changes to the CSV file
        message(f"User '{username_to_remove}' has been removed.")
    else:
        message(f"User '{username_to_remove}' has not been removed.")

def view():
    userlist = "\n".join(usernames)
    message(f"Current Users:\n{userlist}")

def viewpasswords():
    password_list = "\n".join(userpasswords)
    message(f"User Passwords:\n{password_list}")

def removedlog():
    if not os.path.exists(REMOVED_USERS_FILE):
        message("No users have been removed yet.")
        return

    log_entries = []
    with open(REMOVED_USERS_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Make sure the row is not empty
                log_entries.append(f"User: {row[0]}, Removed At: {row[1]}")

    if log_entries:
        log_message = "\n".join(log_entries)
        message(f"Removed Users Log:\n{log_message}")
    else:
        message("No users have been removed yet.")

def adminmenu():
    admin = tk.Toplevel(window)
    admin.title("Manage Users")
    
    def remove():
        username_to_remove = usernameentry.get()
        password_to_remove = passwordentry.get()

        if username_to_remove in usernames:
            num = usernames.index(username_to_remove)
            # Check if the provided password matches
            if userpasswords[num] == password_to_remove:
                confirmremove(username_to_remove, num)
            else:
                message("Incorrect password. Please try again.")
        else:
            message(f"User '{username_to_remove}' not found.")

    tk.Label(admin, text="Enter Username to Remove:").pack(padx=5, pady=5)
    usernameentry = tk.Entry(admin)
    usernameentry.pack(padx=5, pady=5)

    tk.Label(admin, text="Enter Password:").pack(padx=5, pady=5)
    passwordentry = tk.Entry(admin, show='*')
    passwordentry.pack(padx=5, pady=5)

    removebutton = tk.Button(admin, text="Remove User", command=remove)
    removebutton.pack(padx=10, pady=10)

    viewbutton = tk.Button(admin, text="View Users", command=view)
    viewbutton.pack(padx=10, pady=10)

    view_passwords = tk.Button(admin, text="View Passwords", command=viewpasswords)
    view_passwords.pack(padx=10, pady=10)

    viewlog = tk.Button(admin, text="View Removed Users Log", command=removedlog)
    viewlog.pack(padx=10, pady=10)

    closebutton = tk.Button(admin, text="Close", command=admin.destroy)
    closebutton.pack(padx=10, pady=10)

# Main window
window = tk.Tk()
window.title("Manage Users")

# Button to open the admin menu
adminmenu_button = tk.Button(window, text="Manage Users", command=adminmenu)
adminmenu_button.pack(padx=10, pady=10)

window.mainloop()

