import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog 
import csv
import os
from datetime import datetime
from tkinter import ttk

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

def register(root):
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
    USER_DATA_FILE = 'users.csv'
    credFile = "users.csv"
    guestFile = "users.csv"
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
        tk.Button(root, text="Remove User", command=RemoveUser).pack()
    else:
        tk.Button(root, text="View History", command=viewHistory).pack()
        tk.Button(root, text="Search Items", command=searchItems).pack()
        tk.Button(root, text="View Favorites", command=viewFavorites).pack()

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
    tk.Button(root, text="Register", command=lambda: register(root)).pack()
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

    # This is the file name for the borrow requests don't change it without changing the file name (Also the create_csv(): function will need to be updated if you didn't make the csv yet)
    filePath = "BorrowList.csv"

    # This is the file name for the rejected borrow requests
    rejectedFilePath = "rejectedRequests.csv"

    # Function to load all items from the file
    def openFile(file_path=filePath):
        items = []
        try:
            with open(file_path, mode='r') as file:
                read = csv.DictReader(file)
                for i in read:
                    items.append(i)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"File {file_path} not found. Contact cacheMeIfYouCan for help.")
        return items

    # Function to update the status of an req
    def updateStatus(reqID, newStatus):
        items = openFile()
        updated = False

        with open(filePath, mode='w', newline='') as file:
            write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
            write.writeheader()

            for req in items:
                if req['ID'] == reqID:
                    req['Status'] = newStatus
                    updated = True
                write.writerow(req)

        return updated

    # This deletes rejected requests and moves them to the rejected requests csv file
    def deleteRequest(reqID):
        items = openFile()
        rejected_items = openFile(rejectedFilePath)
        with open(filePath, mode='w', newline='') as file:
            write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
            write.writeheader()

            for req in items:
                if req['ID'] == reqID and req['Status'] == "Rejected":
                    rejected_items.append(req)
                else:
                    write.writerow(req)

        with open(rejectedFilePath, mode='w', newline='') as file:
            write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
            write.writeheader()
            write.writerows(rejected_items)

    # Live refresh the treeview if edits are made to the csv file. Also this is where I found how to refresh because I forgot: https://stackoverflow.com/questions/76407618/how-to-refresh-data-in-treeview-in-tkinter row is replacing i.
    def refresh(tree, query=""):
        for row in tree.get_children():
            tree.delete(row)

        items = openFile()
        if query:
            items = [req for req in items if query.lower() in req["Name"].lower()]

        for req in items:
            tree.insert("", "end", values=(req["ID"], req["Name"], req["Producer"], req["Status"]))

    def buttonHandler(tree, action):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error!", "Please select an req to perform this action.")
            return

        reqID = tree.item(selected[0], "values")[0]
        if action == "accept":
            newStatus = "Approved"
            if updateStatus(reqID, newStatus):
                messagebox.showinfo("Success", f"Request {reqID} accepted successfully.")
        else:  # this is essentially action == "reject"
            updateStatus(reqID, "Rejected")
            deleteRequest(reqID)
            messagebox.showinfo("Success", f"Request {reqID} rejected and deleted successfully.")
    
        refresh(tree)

    # GUI 
    def main():
        root = tk.Tk()
        root.title("Borrow Request Management")

        def mainMenu():
            root.destroy()
            # Ethan, this is where you should call your main menu function

        # Treeview if you want more explination here is a good video series https://www.youtube.com/watch?v=YTqDYmfccQU
        columns = ("ID", "Name", "Producer", "Status")
        tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: sortTreeview(tree, _col, False))
            tree.column(col, width=120)
        tree.pack(fill="both", padx=10, pady=10)

        refresh(tree)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Accept", command=lambda: buttonHandler(tree, "accept")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Reject", command=lambda: buttonHandler(tree, "reject")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", command=lambda: refresh(tree)).pack(side="left", padx=5)

        searchFrame = tk.Frame(root)
        searchFrame.pack(pady=10)

        tk.Label(searchFrame, text="Search By:").pack(side="left", padx=5)
        searchArea = ttk.Combobox(searchFrame, values=["ID", "Name", "Producer"], state="readonly")
        searchArea.pack(side="left", padx=5)
        searchArea.current(0)

        dynamicSearch = tk.Entry(searchFrame)
        dynamicSearch.pack(side="left", padx=5)

        # dynamically search the treeview when the user types in the search box. Here is a link for where I found how to do this https://www.youtube.com/watch?v=mSpLnnXeiIc
        def searchRequests(event=None):
            field = searchArea.get()
            query = dynamicSearch.get().strip()
            items = openFile()
            results = [req for req in items if query.lower() in req[field].lower()]

            for row in tree.get_children():
                tree.delete(row)

            for req in results:
                tree.insert("", "end", values=(req["ID"], req["Name"], req["Producer"], req["Status"]))

        dynamicSearch.bind("<KeyRelease>", searchRequests) 
        tk.Button(root, text="Back to Main Menu", command=mainMenu).pack(pady=10)

        root.mainloop()

    # This is me testing a CSV file format for the program
    def createCSV():
        if not os.path.exists(filePath):
            with open(filePath, mode='w', newline='') as file:
                write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
                write.writeheader()
                write.writerows([
                    {"ID": "1", "Name": "Apple", "Producer": "Farm", "Status": "Pending Approval"},
                    {"ID": "2", "Name": "Book", "Producer": "Barnes & Noble", "Status": "Pending Approval"},
                    {"ID": "3", "Name": "Car", "Producer": "Ford", "Status": "Pending Approval"},
                ])
        else:
            print(f"{filePath} already exists. Skipping CSV creation.")

        with open(rejectedFilePath, mode='w', newline='') as file:
            write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
            write.writeheader()

    # Just uncomment this line to create the test CSV, you can only do this once though or you might run in to some annoying issues
    createCSV()

    # Run the GUI
    main()

    
def addUserFeature():
    # Path to the CSV file
    guestFile = "users.csv"

    # Load user data from the CSV file
    def load_users_from_csv():
        try:
            with open(guestFile, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:  # Ensures rows have both username and password
                        user_database[row[0]] = row[1]
                        users[row[0]] = row[1]  # Add to main users dictionary
        except FileNotFoundError:
            with open(guestFile, mode="w") as file:  # Creates the file if it doesn't exist
                pass

    # Save user data to the CSV file
    def save_user_to_csv(username, password):
        with open(guestFile, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

    # User database 
    user_database = {}
    load_users_from_csv() 

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
            users[username] = password  # Add to main users dictionary for login
            save_user_to_csv(username, password)
            messagebox.showinfo("Success", "New Guest User Successfully Created!")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    def display_user_count():
        user_count = len(user_database)
        messagebox.showinfo("User Count", f"There are currently {user_count} guest users.")

    def display_date():
        from datetime import datetime  # Ensure proper import
        current_date = datetime.now().strftime("%Y-%m-%d")
        messagebox.showinfo("Current Date", f"Today's date is: {current_date}")

    # This is where main menu is called
    def main_menu():
        root.destroy()

    # Opens the main window
    root = tk.Tk()
    root.title("Guest User Creation")

    # Creates widgets
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

    # Runs the main event loop
    root.mainloop()


def manageStock():
    # Define the CSV file names
    PRODUCT_CSV = 'products.csv'
    HISTORY_CSV = 'product_history.csv'

    # Ensure the CSV file and history file exist with proper headers if not already there
    def makecsv():
        if not os.path.exists(PRODUCT_CSV):
            with open(PRODUCT_CSV, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Product Name', 'Product ID', 'Producer'])  # Write headers
                initial_products = ['Apple','1','Farm'],['Book','2','Barnes & Noble'],['Car','3','Ford']
                writer.rows(initial_products)

        if not os.path.exists(HISTORY_CSV):
            with open(HISTORY_CSV, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Action', 'Product Name', 'Product ID', 'Producer'])

# Load product data from CSV
    def load_data():
        products = []
        if os.path.exists(PRODUCT_CSV):
            with open(PRODUCT_CSV, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    products.append(row)
        return products

# Write product data to CSV
    def save_data(products):
        with open(PRODUCT_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Product ID', 'Producer'])  # Write headers
            writer.writerows(products)

# Log product actions to the history file
    def log_history(action, name, pid, producer):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(HISTORY_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, action, name, pid, producer])

# Is created so there can easily be a message made simply by calling "message(x)".
    def message(message):
        messagebox.showinfo("Information", message)

# Main Menu function
    def MainMenu():
        window = tk.Tk()
        window.title("Main Menu")

        def manage_options():
            manage(window)

        managebutton = tk.Button(window, text="Manage Products", command=manage_options)
        managebutton.pack(padx=10, pady=10)

        def view():
            view_window = tk.Toplevel(window)
            view_window.title("View Products")

        # Load the products from CSV and display them
            products = load_data()
            if len(products) > 0:
                for product in products:
                    product_info = f"Name: {product[0]}, ID: {product[1]}, Producer: {product[2]}"
                    tk.Label(view_window, text=product_info).pack(padx=10, pady=5)
            else:
                tk.Label(view_window, text="No products available.").pack(padx=10, pady=10)

            closebutton_view = tk.Button(view_window, text="Close", command=view_window.destroy)
            closebutton_view.pack(padx=10, pady=10)

        viewbutton = tk.Button(window, text="View Products", command=view)
        viewbutton.pack(padx=10, pady=10)

        def view_history():
            history_window = tk.Toplevel(window)
            history_window.title("View Action History")

        # Load the history from the history file
            if os.path.exists(HISTORY_CSV):
                with open(HISTORY_CSV, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip the header row
                    for row in reader:
                        timestamp, action, name, pid, producer = row
                        history_info = f"{timestamp} - {action}: {name} (ID: {pid}) by {producer}"
                        tk.Label(history_window, text=history_info).pack(padx=10, pady=5)
            else:
                tk.Label(history_window, text="No action history available.").pack(padx=10, pady=10)

            closebutton_history = tk.Button(history_window, text="Close", command=history_window.destroy)
            closebutton_history.pack(padx=10, pady=10)

        historybutton = tk.Button(window, text="View Action History", command=view_history)
        historybutton.pack(padx=10, pady=10)

        window.mainloop()

# Manage products window
    def manage(window):
        manage_window = tk.Toplevel(window)
        manage_window.title("Manage Products")

        def add():
            name2 = name.get()
            pid2 = pid.get()
            producer2 = producer.get()
            try:
                pid2 = int(pid2)
                # Load existing products from CSV
                products = load_data()
                # Check if the ID already exists
                for product in products:
                    if int(product[1]) == pid2:
                        message("Item with this ID already exists.")
                        return
                # Add the new product
                products.append([name2, str(pid2), producer2])
                save_data(products)
                log_history('Added', name2, pid2, producer2)
                message("Addition complete.")
            except ValueError:
                message("Please input a valid ID.")


        def delete():
            pid2 = pid.get()
            try:
                pid2 = int(pid2)
                products = load_data()
                for product in products:
                    if int(product[1]) == pid2:
                        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {product[0]} (ID: {product[1]})?"):
                            products.remove(product)
                            save_data(products)
                            log_history('Deleted', product[0], pid2, product[2])
                            message("Deletion complete.")
                        return
                message("Product does not exist.")
            except ValueError:
                message("Please input a valid ID.")
    
        def edit():
            pid2 = pid.get()
            try:
                pid2 = int(pid2)
                # Load existing products from CSV
                products = load_data()
                for i, product in enumerate(products):
                    if int(product[1]) == pid2:
                        name2 = name.get()
                        producer2 = producer.get()
                        npid2 = npid.get()
                        npid2 = int(npid2)
                        # Edit the product
                        old_product = products[i]
                        products[i] = [name2, str(npid2), producer2]
                        save_data(products)
                        log_history('Edited', name2, npid2, producer2)
                        message("Edit complete.")
                        return
                message("Product ID does not exist.")
            except ValueError:
                message("Please input a valid ID.")

        # Create the input for add/delete/edit
        tk.Label(manage_window, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        name = tk.Entry(manage_window)
        name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(manage_window, text="Product ID:").grid(row=1, column=0, padx=5, pady=5)
        pid = tk.Entry(manage_window)
        pid.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(manage_window, text="Producer:").grid(row=2, column=0, padx=5, pady=5)
        producer = tk.Entry(manage_window)
        producer.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(manage_window, text="New Product ID (for edit):").grid(row=3, column=0, padx=5, pady=5)
        npid = tk.Entry(manage_window)
        npid.grid(row=3, column=1, padx=5, pady=5)

    # Buttons to add/delete/edit products
        additembutton = tk.Button(manage_window, text="Add Item", command=add)
        additembutton.grid(row=4, column=0, padx=5, pady=5)

        deleteitembutton = tk.Button(manage_window, text="Delete Item", command=delete)
        deleteitembutton.grid(row=4, column=1, padx=5, pady=5)

        edititembutton = tk.Button(manage_window, text="Edit Item", command=edit)
        edititembutton.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        closebutton = tk.Button(manage_window, text="Close", command=manage_window.destroy)
        closebutton.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

#Make the product file and history file if they don't exist
    makecsv()

# Start the warehouse management
    MainMenu()

def searchItems():
    # Zach and Thomas' code
    # here I am defining the global variables for the buy/borrow command so that they can be called later in the code
    BorB = ""
    DurB = ""
    DateB = ""

    filePath = "products.csv" #You can edit the name it doesn't matter

    # Function to create a favorites CSV file if it does not exist
    def createFavoritesCSV():
        if not os.path.exists("favorites.csv"):
            with open("favorites.csv", "w", newline="") as file:
                write = csv.writer(file)
                write.writerow(["ID", "Name", "Producer"])

    # Function to load all items from the file
    def openFile():
        items = []
        try:
            with open(filePath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    items.append(row)
        except FileNotFoundError:
            messagebox.showerror("File Error", f"The file {filePath} was not found.")
        except Exception as errorName:
            messagebox.showerror("Error", f"An error occurred: {errorName}")
        return items

    # Function to perform the search
    def searchItems(search_type, search_query):
        items = openFile()
        return [item for item in items if  search_query.lower() == item[search_type].lower()]

    # Function to refresh the search results
    def refreshSearch():
        performSearch()

    # Function to add an item to favorites and create or write to a csv file
    def addToFavorites(item=None):
        try:
            if item is None:
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Error", "Please select an item to add to favorites!")
                    return
                item_values = tree.item(selected_item[0], "values")
                item = {"Product ID": item_values[0], "Product Name": item_values[1], "Producer": item_values[2]}

            fileExists = os.path.exists("favorites.csv")
            with open("favorites.csv", "a", newline="") as file:
                write = csv.writer(file)
                if not fileExists:
                    write.writerow(["Product ID", "Product Name", "Producer"])
                write.writerow([item["Product ID"], item["Product Name"], item["Producer"]])
        
            messagebox.showinfo("Favorites", "Item added to favorites successfully!")
        except Exception as errorName:
            messagebox.showerror("Error", f"An error occurred: {errorName}")

    # Below here is all code added by myself (Thomas) for the buy and borrow functions.

    def requestToB(item=None):
        global CB
        global BorB
        global DurB
        CB = 0
        try:
            if item is None:
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Error", "Please select an item to request")
                    return
                item_values = tree.item(selected_item[0], "values")
                item = {"Product ID": item_values[0], "Product Name": item_values[1], "Producer": item_values[2]}
        
            fileExists = os.path.exists("BorrowList.csv") 
            # commands to select whether to buy or borrow an item
            BuyOrBorrowWindow()
            DateB = datetime.now()
            DateB = DateB.date()
        
            if CB == 0:
                with open("BorrowList.csv", "a", newline="") as file:
                    write = csv.writer(file)
                    if not fileExists:
                        write.writerow(["Product ID", "Product Name", "Producer", "Buy or borrow", "Borrow duration", "Date of request", "Approval by Admin"])
                    write.writerow([item["Product ID"], item["Product Name"], "PENDING"])
            
                # this segment adds a copy to the user history list 
                with open("UserHistory.csv", "a", newline="") as file:
                    write = csv.writer(file)
                    if not fileExists:
                        write.writerow(["Product ID", "Product Name", "Producer", "Buy or borrow", "Borrow duration", "Date of request"])
                    write.writerow([item["Product ID"], item["Product Name"], item["Producer"], BorB, f"{DurB} days", DateB])
                
                messagebox.showinfo("Buy/Borrow list", "Item requested!")
            elif CB == 1:
                messagebox.showinfo("Buy/Borrow list", "Request denied, you can only request 3 items at a time!")
            
        except Exception as errorName:
            messagebox.showerror("Error", f"An error occurred: {errorName}")

    
    # creating a custom class for a 2 option window.
    class OptionsWindow(simpledialog.Dialog):
        def body(self, master):
            self.result= None
            tk.Label(master, text="Are you requesting this item to buy or to borrow?").grid(row=0)
            tk.Button(master, text="Buy", command=BuyCmd).grid(row=1)
            tk.Button(master, text="Borrow", command=BorrowCmd).grid(row=2)
            tk.Label(master, text="Press OK to confirm your choice!").grid(row=3)
        
    # function to call the options window
    def BuyOrBorrowWindow():
        OptionsWindow(root, title="Buy or Borrow this item?")

  
    # fuctions for the buttons to buy or borrow -- and setting of the appropriate variables
    def BuyCmd():
        global BorB
        global DurB
        BorB = "Buy"
        DurB = "N/A"
    def BorrowCmd():
        global BorB
        global DurB
        BorB = "Borrow"
        DurB = simpledialog.askstring("Input","How many days would you like to borrow this item for?", parent = root)


    #End of Thomas' code

    # Function to load all users from csv
    def loadAllUsers():
        # Clear existing items first
        for item in tree.get_children():
            tree.delete(item)
        items = openFile()
        for item in items:
            tree.insert("", tk.END, values=(item["Product ID"], item["Product Name"], item["Producer"]))

    # Function for the search button
    def performSearch(event=None):
        search_type = searchOption.get()
        search_query = searchEntry.get().strip()

        if not search_query:
            loadAllUsers()
            return

        search_results = searchItems(search_type, search_query)

        for row in tree.get_children():
            tree.delete(row)
        for item in search_results:
            tree.insert("", tk.END, values=(item["Product ID"], item["Product Name"], item["Producer"]))

    # Function to clear search and return to main menu
    def clearSearch():
        searchEntry.delete(0, tk.END)
        loadAllUsers()

    # Main application window you can rezie it if you want but this is pretty good size
    root = tk.Tk()
    root.title("Regular User Search")
    root.geometry("600x500")

    # Search frame
    searchFrame = tk.Frame(root)
    searchFrame.pack(pady=10)

    # Search Options/ buttons for diffrent types of data
    tk.Label(searchFrame, text="Search By:").grid(row=0, column=0, padx=5)

    searchOption = tk.StringVar(value="Product ID")
    tk.Radiobutton(searchFrame, text="Product ID", variable=searchOption, value="Product ID").grid(row=0, column=1, padx=5)
    tk.Radiobutton(searchFrame, text="Product Name", variable=searchOption, value="Product Name").grid(row=0, column=2, padx=5)
    tk.Radiobutton(searchFrame, text="Producer", variable=searchOption, value="Producer").grid(row=0, column=3, padx=5)

    # Search entry
    tk.Label(searchFrame, text="Enter Search Query:").grid(row=1, column=0, padx=5)
    searchEntry = tk.Entry(searchFrame)
    searchEntry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
    searchEntry.bind("<KeyRelease>", performSearch)  

    # Here are all the cool buttons
    buttonFrame = tk.Frame(root)
    buttonFrame.pack(pady=10)

    # Removed the search button
    tk.Button(buttonFrame, text="Add to Favorites", command=addToFavorites).grid(row=0, column=0, padx=5)
    tk.Button(buttonFrame, text="Clear Search", command=clearSearch).grid(row=0, column=1, padx=5)
    tk.Button(buttonFrame, text="Refresh", command=refreshSearch).grid(row=0, column=2, padx=5)
    tk.Button(buttonFrame, text="Buy/Borrow", command=requestToB).grid(row=0, column=4, padx=5)
    tk.Button(buttonFrame, text="Main Menu", command=root.destroy).grid(row=0, column=3, padx=5)

    # Search results treeview
    treeFrame = tk.Frame(root)
    treeFrame.pack(pady=10, fill=tk.BOTH, expand=False)  

    tree = ttk.Treeview(treeFrame, columns=("Product ID", "Product Name", "Producer"), show="headings", height=10) 
    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Producer", text="Producer")
    tree.pack(side="left", fill=tk.BOTH, padx=10, pady=10) 

    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Load all users for treeview
    loadAllUsers()

    # This is me testing a CSV file format for the program
    def createCSV():
        if not os.path.exists(filePath):
            with open(filePath, mode='w', newline='') as file:
                write = csv.DictWriter(file, fieldnames=["Product ID", "Product Name", "Producer"])
                write.writeheader()
                write.writerows([
                    {"Product ID": "1", "Product Name": "Apple", "Producer": "Farm"},
                    {"Product ID": "2", "Product Name": "Book", "Producer": "Barnes & Noble"},
                    {"Product ID": "3", "Product Name": "Car", "Producer": "Ford"},
                ])
        else:
            print(f"{filePath} already exists. Skipping CSV creation.")
    # Just uncomment this line to create the test CSV, you can only do this once though or you might run in to some annoying issues
    createCSV()

    # Run the Application
    root.mainloop()

def viewHistory():
    # messagebox.showinfo("View History", "Placeholder for View History functionality.")
    filename = "UserHistory.csv"

    root = tk.Tk()
    root.title("User view history")
    root.geometry("750x750")

    tree = ttk.Treeview(root)

    tree['columns'] = ['ID','Name','Producer','Buy or Borrow','Borrow Duration','Date of Request']
    # columns
    tree.column("#0", width=0, minwidth=0)
    tree.column("ID", anchor="w", width=120, minwidth=25)
    tree.column("Name", anchor="center", width=120, minwidth=25)
    tree.column("Producer", anchor="w", width=120, minwidth=25)
    tree.column("Buy or Borrow", anchor="w", width=120, minwidth=25)
    tree.column("Borrow Duration", anchor="w", width=120, minwidth=25)
    tree.column("Date of Request", anchor="w", width=120, minwidth=25)

    #headings
    tree.heading("#0", text="", anchor="w")
    tree.heading("ID", text="Product ID", anchor="w")
    tree.heading("Name", text="Product Name", anchor="center")
    tree.heading("Producer", text="Product Producer", anchor="w")
    tree.heading("Buy or Borrow", text="Buy or Borrow", anchor="w")
    tree.heading("Borrow Duration", text="Borrow Duration", anchor="w")
    tree.heading("Date of Request", text="Date of Request", anchor="e")

    # Cearing the tree view (sub-function of refresh)
    def ListClear():
        for item in tree.get_children():
            tree.delete(item)

    # refreshing the tree view for edits made in other windows -- this is also called to instantly refresh the view after deleting an entry
    def ListRefresh():
        ListClear()
        with open(filename, 'r',) as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row))

    tree.grid(row=0, column=0)

    #this is where main menu is called
    def mainMenu():
        root.destroy()

    def delHistory():
        select_row = tree.selection()[0] #selected row
        RIndex = tree.index(select_row)
        
        
        with open("UserHistory.csv","r") as file:
            reader = csv.reader(file)
            rows = list(reader)
           
        del rows[RIndex]
        
        # rewrites the file with 
        with open("UserHistory.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
            
        ListRefresh() #refreshes the list

        messagebox.showinfo("History", "Item Deleted! Refresh List if change is not present")

    tk.Label(root,text="Press refresh to see values.").grid(row=1, column=0)

    btn_refresh = tk.Button(root, text="Refresh List", command= ListRefresh)
    btn_refresh.grid(row=2, column=0)

    btn_return = tk.Button(root, text="Return to Main Menu", command= mainMenu)
    btn_return.grid(row=3, column=0)

    btn_delete = tk.Button(root, text="Delete item from history", command= delHistory)
    btn_delete.grid(row=4, column=0)

    root.mainloop()

def viewFavorites():
    filename= 'favorites.csv'

    # GUI setup
    root = tk.Tk()
    root.title("View Favorites")
    root.geometry("700x400")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # global treeview widget to use for multiple functions
    info_tree = ttk.Treeview(root, columns=("Product ID", "Product Name", "Product Producer"), show="headings")

    # user-friendly enhancements
    frame_buttons = tk.Frame(root)
    frame_buttons.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    frame_treeview = tk.Frame(root)
    frame_treeview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    vsb = ttk.Scrollbar(frame_treeview, orient="vertical", command=info_tree.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    info_tree.configure(yscrollcommand=vsb.set)

    def clearTreeview():
        for item in info_tree.get_children():
            info_tree.delete(item)

    # configure treeview widget and columns and headings
    info_tree.grid(row=2, column=0, columnspan=3, sticky="ew")
    info_tree.heading("Product ID", text="Product ID", command=lambda: sortTreeview("Product ID"))
    info_tree.column("Product ID", width=100)
    info_tree.heading("Product Name", text="Product Name", command=lambda: sortTreeview("Product Name"))
    info_tree.column("Product Name", width=150)
    info_tree.heading("Product Producer", text="Product Producer", command=lambda: sortTreeview("Product Producer"))
    info_tree.column("Product Producer", width=150)
    clearTreeview()
    # read the csv and add into the treeview
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            info_tree.insert("", tk.END, values=row)

    # Global variable to keep track of sorting state
    sort_order = {'Product ID': False, 'Product Name': False, 'Product Producer': False}

    # helper function that clears the treeview
    

    def viewFavorites():
        # configure treeview widget and columns and headings
        info_tree.grid(row=2, column=0, columnspan=3, sticky="ew")
        info_tree.heading("Product ID", text="Product ID", command=lambda: sortTreeview("Product ID"))
        info_tree.column("Product ID", width=100)
        info_tree.heading("Product Name", text="Product Name", command=lambda: sortTreeview("Product Name"))
        info_tree.column("Product Name", width=150)
        info_tree.heading("Product Producer", text="Product Producer", command=lambda: sortTreeview("Product Producer"))
        info_tree.column("Product Producer", width=150)
        clearTreeview()
        # read the csv and add into the treeview
        with open(filename, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                info_tree.insert("", tk.END, values=row)

    def removeFavorites():
        # get selected item
        select_item = info_tree.selection()
        if not select_item:
            messagebox.showwarning("No Selection", "Please select a row to remove.")
            return
        # get the values of the selected items
        select_values = info_tree.item(select_item, "values")
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove?")
        if confirm:
            info_tree.delete(select_item)
            # update csv file
            with open(filename, mode='r') as csvfile:
                rows = list(csv.reader(csvfile))
            # filter out row to be removed
            rows = [row for row in rows if row != list(select_values)]
            # rewrite csv file
            with open(filename, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
                messagebox.showinfo("Success", f"Removed {select_values[1]} successfully!")
        else:
            return

    def searchFavorites():
        search_query = search_entry.get().lower()
        if not search_query:
            messagebox.showwarning("Empty Search", "Please enter a search term.")
            return
        clearTreeview()
        # Read the csv file and display matching rows
        with open(filename, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                if any(search_query in cell.lower() for cell in row):  # Case-insensitive search
                    info_tree.insert("", tk.END, values=row)

    def sortTreeview(column):
        data = []
        for child in info_tree.get_children():
            data.append(info_tree.item(child, "values"))
        
        column_index = info_tree["columns"].index(column)
        
        # Toggle sorting order
        reverse = sort_order[column]
        sort_order[column] = not reverse  # Toggle the sort order for next time
        
        # Check the column and sort accordingly
        if column == "Product ID":
            data.sort(key=lambda x: int(x[column_index]), reverse=reverse)  # Sort Product ID as integer
        else:
            data.sort(key=lambda x: x[column_index].lower(), reverse=reverse)  # Sort as string (case insensitive)
        
        # Clear the treeview and reinsert the sorted data
        clearTreeview()
        for row in data:
            info_tree.insert("", tk.END, values=row)

    # function to main menu but this is a placeholder
    def mainMenu():
        root.destroy()

    # Widgets
    search_label = tk.Label(frame_buttons, text="Search Products:")
    search_label.grid(row=1, column=0, padx=10, pady=5)

    search_entry = tk.Entry(frame_buttons, width=30)
    search_entry.grid(row=1, column=1, padx=10, pady=5)

    # Buttons
    btn_show = tk.Button(frame_buttons, text="View Favorites", command=viewFavorites)
    btn_show.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    btn_search = tk.Button(frame_buttons, text="Search", command=searchFavorites)
    btn_search.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

    btn_remove = tk.Button(frame_buttons, text="Remove Selected Product", command=removeFavorites)
    btn_remove.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

    btn_return = tk.Button(frame_buttons, text="Return to Main Menu", command=mainMenu)  # Main menu placeholder
    btn_return.grid(row=0, column=2, pady=10, padx=10, sticky="ew")

def RemoveUser():
    # File names for storing user data and removed user logs
    USER_DATA_FILE = 'users.csv'
    REMOVED_USERS_FILE = 'removed_users_log.csv'

    # Load user data from the CSV file
    def userdata():
        global usernames, userpasswords
        if not os.path.exists(USER_DATA_FILE):
            return [], [] # returns empty lists if the file does not exist
    
        usernames, passwords = [], []
        with open(USER_DATA_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # ensures the row has three elements
                    usernames.append(row[0])
                    passwords.append(row[1])
        return usernames, passwords

# Save user data to the CSV file
    def savedata():
        with open(USER_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            for i in range(len(usernames)):
                writer.writerow([usernames[i], userpasswords[i]])

# Log removed user data
    def logremoved(username):
        with open(REMOVED_USERS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the username and the timestamp of removal
            writer.writerow([username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    usernames, userpasswords= userdata()

    def message(msg):
        messagebox.showinfo("Information", msg)

    def confirmremove(username_to_remove, num):
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove user '{username_to_remove}'?")
        if confirm:
            logremoved(username_to_remove)
        
            usernames.pop(num)
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
    
    root.protocol("WM_DELETE_WINDOW", onclose)
    
    setupGui(root)
    root.after(100, showWelcomeMessage) 
    root.mainloop()

runApp()
