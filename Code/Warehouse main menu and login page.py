import tkinter as tk
from tkinter import messagebox
import csv
import os

credFile = "users.csv"
users = {}

def loadUsers():
    if not os.path.exists(credFile):
        with open(credFile, "w", newline="") as f:
            pass  
    else:
        try:
            with open(credFile, "r") as f:
                for row in csv.reader(f):
                    if len(row) == 2:
                        users[row[0]] = row[1]
        except Exception as e:
            messagebox.showerror("Error", f"Error reading user file: {e}")


def saveUser(user, pw):
    #Save a new user to the CSV file.
    try:
        with open(credFile, "a", newline="") as f:
            csv.writer(f).writerow([user, pw])
    except Exception as e:
        messagebox.showerror("Error", f"Error saving user: {e}")

def setupGui(root):
    #Set up the login and register GUI
    adminUser = "admin"
    adminPw = "1234"
    users[adminUser] = adminPw  # Add admin credentials by default

    def login():
        #Prompt the user screen and handle login
        user = userEntry.get()
        pw = pwEntry.get()

        if user in users and users[user] == pw:
            if user == adminUser:
                messagebox.showinfo("Login", "Welcome, Admin!")
                showMenu("admin")
            else:
                messagebox.showinfo("Login", f"Welcome, {user}!")
                showMenu("user")
        else:
            messagebox.showerror("Error", "Invalid login.")

    def register():
        #Open the registration window to create a new account
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

    def showMenu(userType):
        #Display the menu depending on the Uset ype, Admin or Regular
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text=f"Menu - {userType.capitalize()}").pack()
        if userType == "admin":
            options = ["View Requests", "Add User", "Manage Stock"]
        else:
            options = ["View History", "Search Items", "Buy"]

        for opt in options:
            tk.Button(root, text=opt, command=lambda o=opt: messagebox.showinfo("Option", f"{o} clicked")).pack()

    #Login screen widgets
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
    #Run the code
    loadUsers()
    root = tk.Tk()
    root.title("Login")
    root.geometry("400x300")
    setupGui(root)
    root.mainloop()

runApp()