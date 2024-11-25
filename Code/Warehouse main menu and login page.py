import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

# File paths
credFile = "users.csv"
loginLogFile = "loginLog.csv"

# Data storage
users = {}
loginAttempts = {}

# Configuration
MAX_ATTEMPTS = 3

# Function Definitions
def loadUsers():
    #Load users from the credentials file into memory.
    if os.path.exists(credFile):
        try:
            with open(credFile, "r") as f:
                for row in csv.reader(f):
                    if len(row) == 2:
                        users[row[0]] = row[1]
        except Exception as e:
            messagebox.showerror("Error", f"Error reading user file: {e}")

def saveUser(user, pw):
    #Save a new user to the credentials file.#
    try:
        with open(credFile, "a", newline="") as f:
            csv.writer(f).writerow([user, pw])
    except Exception as e:
        messagebox.showerror("Error", f"Error saving user: {e}")

def logLogin(user, success):
    #Log user login attempts.
    try:
        with open(loginLogFile, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([user, "Success" if success else "Failure", datetime.now()])
    except Exception as e:
        messagebox.showerror("Error", f"Error logging login: {e}")

def limitLoginAttempts(user):
    #Enforce limited login attempts for security.
    if user not in loginAttempts:
        loginAttempts[user] = 0
    loginAttempts[user] += 1

    if loginAttempts[user] >= MAX_ATTEMPTS:
        messagebox.showerror("Error", "Too many failed login attempts!")
        return False  # Prevent further attempts
    return True

def resetPassword(root):
    #Allow a user to reset their password.
    def updatePassword():
        username = usernameEntry.get().strip()
        oldPassword = oldPwEntry.get().strip()
        newPassword = newPwEntry.get().strip()

        if username not in users or users[username] != oldPassword:
            messagebox.showerror("Error", "Invalid username or old password.")
        else:
            users[username] = newPassword
            saveUser(username, newPassword)
            messagebox.showinfo("Success", "Password updated successfully!")
            resetWin.destroy()

    resetWin = tk.Toplevel(root)
    resetWin.title("Reset Password")
    resetWin.geometry("300x200")
    tk.Label(resetWin, text="Username").pack()
    usernameEntry = tk.Entry(resetWin)
    usernameEntry.pack()
    tk.Label(resetWin, text="Old Password").pack()
    oldPwEntry = tk.Entry(resetWin, show="*")
    oldPwEntry.pack()
    tk.Label(resetWin, text="New Password").pack()
    newPwEntry = tk.Entry(resetWin, show="*")
    newPwEntry.pack()
    tk.Button(resetWin, text="Update Password", command=updatePassword).pack()

def logout(root):
    #Logout the current user and return to the login screen.
    for widget in root.winfo_children():
        widget.destroy()
    setupGui(root)

def displayProfile(currentUser):
    #Display the current user's profile information.
    userType = "Admin" if currentUser == "admin" else "User"
    messagebox.showinfo("Profile Info", f"Username: {currentUser}\nType: {userType}")

def goBackToLogin(root):
    #Return to the main login screen.
    for widget in root.winfo_children():
        widget.destroy()
    setupGui(root)

def addMenuFeatures(root, userType, currentUser):
    if userType == "admin":
        tk.Button(root, text="Log Out", command=lambda: logout(root)).pack()
        tk.Button(root, text="Display Profile", command=lambda: displayProfile(currentUser)).pack()
    else:
        tk.Button(root, text="Log Out", command=lambda: goBackToLogin(root)).pack()
        tk.Button(root, text="Display Profile", command=lambda: displayProfile(currentUser)).pack()

# Main GUI Setup
def setupGui(root):
    adminUser = "admin"
    adminPw = "1234"
    users[adminUser] = adminPw  # Add admin credentials by default

    def login():
        user = userEntry.get().strip()
        pw = pwEntry.get().strip()

        if user not in users or users[user] != pw:
            if limitLoginAttempts(user):
                logLogin(user, False)
                messagebox.showerror("Error", "Invalid login.")
        else:
            logLogin(user, True)
            if user == adminUser:
                showMenu("admin", user)
            else:
                showMenu("user", user)

    def register():
        #Open the registration window.
        def addUser():
            #Register a new user.
            newUser = regUser.get().strip()
            newPw = regPw.get().strip()

            if not newUser or not newPw:
                messagebox.showerror("Error", "Fill all fields!")
            elif newUser in users:
                messagebox.showerror("Error", "User already exists!")
            else:
                users[newUser] = newPw
                saveUser(newUser, newPw)
                messagebox.showinfo("Success", "User registered successfully!")
                regWin.destroy()

        regWin = tk.Toplevel(root)
        regWin.title("Register")
        regWin.geometry("300x200")
        tk.Label(regWin, text="New Username").pack()
        regUser = tk.Entry(regWin)
        regUser.pack()
        tk.Label(regWin, text="New Password").pack()
        regPw = tk.Entry(regWin, show="*")
        regPw.pack()
        tk.Button(regWin, text="Register", command=addUser).pack()

    def showMenu(userType, currentUser):
        #Display the menu based on user type.
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text=f"Menu - {userType.capitalize()}").pack()
        if userType == "admin":
            options = ["View Requests", "Add User", "Manage Stock"]
        else:
            options = ["View History", "Search Items", "Buy"]

        for opt in options:
            tk.Button(root, text=opt, command=lambda o=opt: messagebox.showinfo("Option", f"{o} clicked")).pack()

        addMenuFeatures(root, userType, currentUser)

    # Login screen widgets
    tk.Label(root, text="Warehouse Login").pack()
    tk.Label(root, text="Username").pack()
    userEntry = tk.Entry(root)
    userEntry.pack()
    tk.Label(root, text="Password").pack()
    pwEntry = tk.Entry(root, show="*")
    pwEntry.pack()
    tk.Button(root, text="Login", command=login).pack()
    tk.Button(root, text="Register", command=register).pack()

def runApp():
    #Run the application.
    loadUsers()
    root = tk.Tk()
    root.title("Login")
    root.geometry("400x300")
    setupGui(root)
    root.mainloop()

# Run the Application
runApp()
