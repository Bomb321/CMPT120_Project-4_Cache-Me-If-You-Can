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
blockedUsers = {}  # Track blocked users

# Configuration
MAX_ATTEMPTS = 3

# Function Definitions
def loadUsers():
    if os.path.exists(credFile):
        try:
            with open(credFile, "r") as f:
                for row in csv.reader(f):
                    if len(row) == 2:
                        users[row[0]] = row[1]
        except Exception as e:
            messagebox.showerror("Error", f"Error reading user file: {e}")

def saveUser(user, pw):
    try:
        with open(credFile, "a", newline="") as f:
            csv.writer(f).writerow([user, pw])
    except Exception as e:
        messagebox.showerror("Error", f"Error saving user: {e}")

def logLogins(user, success):
    try:
        with open(loginLogFile, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([user, "Success" if success else "Failure", datetime.now()])
    except Exception as e:
        messagebox.showerror("Error", f"Error logging login: {e}")

def limitLoginAttempts(user):
    if user not in loginAttempts:
        loginAttempts[user] = 0
    loginAttempts[user] += 1

    if loginAttempts[user] >= MAX_ATTEMPTS:
        blockedUsers[user] = True  # Block user after MAX_ATTEMPTS
        messagebox.showerror("Error", "Too many failed login attempts! Your account is now blocked.")
        return False
    return True

def viewLoginLog(root):
    if not os.path.exists(loginLogFile):
        messagebox.showinfo("Info", "No login logs available.")
        return

    logWin = tk.Toplevel(root)
    logWin.title("Login Log")
    logWin.geometry("500x300")
    tk.Label(logWin, text="Login Log").pack()

    logText = tk.Text(logWin, wrap=tk.WORD, state=tk.DISABLED, width=60, height=15)
    logText.pack()

    try:
        with open(loginLogFile, "r") as f:
            logData = f.readlines()

        logText.config(state=tk.NORMAL)
        logText.delete(1.0, tk.END)
        for entry in logData:
            logText.insert(tk.END, entry)
        logText.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Error reading login log: {e}")

def register():
    def addUser():
        newUser = regUser.get().strip()
        newPw = regPw.get().strip()

        if not newUser or not newPw:
            messagebox.showerror("Error", "Fill all fields!")
        elif len(newPw) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
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
    tk.Label(regWin, text="New Password (at least 8 characters)").pack()
    regPw = tk.Entry(regWin, show="*")
    regPw.pack()
    tk.Button(regWin, text="Register", command=addUser).pack()

def logout(root):
    for widget in root.winfo_children():
        widget.destroy()
    setupGui(root)

def displayProfile(currentUser):
    userType = "Admin" if currentUser == "admin" else "User"
    messagebox.showinfo("Profile Info", f"Username: {currentUser}\nType: {userType}")

def addMenuFeatures(root, userType, currentUser):
    if userType == "admin":
        tk.Button(root, text="Log Out", command=lambda: logout(root)).pack()
        tk.Button(root, text="Display Profile", command=lambda: displayProfile(currentUser)).pack()
        tk.Button(root, text="View Login Log", command=lambda: viewLoginLog(root)).pack()
    else:
        tk.Button(root, text="Log Out", command=lambda: logout(root)).pack()
        tk.Button(root, text="Display Profile", command=lambda: displayProfile(currentUser)).pack()

def showMenu(userType, currentUser, root):  # Defined globally now
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Menu - {userType.capitalize()}").pack()

    if userType == "admin":
        tk.Button(root, text="View Requests", command=viewRequests).pack()
        tk.Button(root, text="Add User", command=addUserFeature).pack()
        tk.Button(root, text="Manage Stock", command=manageStock).pack()
    else:
        tk.Button(root, text="View History", command=viewHistory).pack()
        tk.Button(root, text="Search Items", command=searchItems).pack()
        tk.Button(root, text="Buy", command=buyItems).pack()

    addMenuFeatures(root, userType, currentUser)

def setupGui(root):
    adminUser = "admin"
    adminPw = "admin1234"
    users[adminUser] = adminPw  # Add admin credentials by default

    def login():
        user = userEntry.get().strip()
        pw = pwEntry.get().strip()

        if user in blockedUsers:
            messagebox.showerror("Error", "Your account is temporarily blocked due to too many failed attempts.")
            return

        if user not in users or users[user] != pw:
            if limitLoginAttempts(user):
                logLogins(user, False)
                messagebox.showerror("Error", "Invalid login.")
        else:
            logLogins(user, True)
            if user == adminUser:
                showMenu("admin", user, root)
            else:
                showMenu("user", user, root)

    # Ensure that these elements are added to the root window only once
    tk.Label(root, text="Warehouse Login").pack()
    tk.Label(root, text="Username").pack()
    userEntry = tk.Entry(root)
    userEntry.pack()
    tk.Label(root, text="Password").pack()
    pwEntry = tk.Entry(root, show="*")
    pwEntry.pack()

    # Ensure buttons remain active and functional
    tk.Button(root, text="Login", command=login).pack()
    tk.Button(root, text="Register", command=register).pack()
    tk.Button(root, text="Reset Password", command=lambda: resetPassword(root)).pack()

def resetPassword(root):
    def updatePassword():
        username = usernameEntry.get().strip()
        oldPassword = oldPwEntry.get().strip()
        newPassword = newPwEntry.get().strip()

        if username not in users or users[username] != oldPassword:
            messagebox.showerror("Error", "Invalid username or old password.")
        elif len(newPassword) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
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
    tk.Label(resetWin, text="New Password (at least 8 characters)").pack()
    newPwEntry = tk.Entry(resetWin, show="*")
    newPwEntry.pack()
    tk.Button(resetWin, text="Update Password", command=updatePassword).pack()

# Define the missing functions globally
def viewRequests():
    messagebox.showinfo("View Requests", "Placeholder for View Requests functionality.")

def addUserFeature():
    messagebox.showinfo("Add User", "Placeholder for Add User functionality.")

def manageStock():
    messagebox.showinfo("Manage Stock", "Placeholder for Manage Stock functionality.")

def searchItems():
    messagebox.showinfo("Search Items", "Placeholder for Search Items functionality.")

def viewHistory():
    messagebox.showinfo("View History", "Placeholder for View History functionality.")

def buyItems():
    messagebox.showinfo("Buy Items", "Placeholder for Buy Items functionality.")

def showWelcomeMessage():
    # Displays a welcome message when the application starts.
    messagebox.showinfo("Welcome", "Welcome to the Warehouse Management System!\nPlease log in or register to proceed.")

def runApp():
    loadUsers()
    root = tk.Tk()
    root.title("Login")
    root.geometry("400x300")
    
    
    def onclose():
        messagebox.showinfo("Goodbye", "Thank you for using the program!")
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    setupGui(root)
    root.after(100, showWelcomeMessage) 
    root.mainloop()

runApp()



