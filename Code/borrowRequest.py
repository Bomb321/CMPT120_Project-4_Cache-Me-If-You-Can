import tkinter as tk
from tkinter import ttk, messagebox
import csv

# This is the file name for the borrow requests don't change it without changing the file name (Also the create_csv(): function will need to be updated if you didn't make the csv yet)
filePath = "borrowRequests.csv"

# Function to load all items from the file
def openFile():
    items = []
    try:
        with open(filePath, mode='r') as file:
            read = csv.DictReader(file)
            for i in read:
                items.append(i)
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "File not found. Contact cacheMeIfYouCan for help.")
    return items

# Function to update the status of an req
def updateStatus(reqID, newStatus):
    items = openFile()
    updated = False

    with open(filePath, mode='w', newline='') as file:
        write = csv.DictWriter(file, fieldnames=["ID", "Name", "Manufacturer", "Status"])
        write.writeheader()

        for req in items:
            if req['ID'] == reqID:
                req['Status'] = newStatus
                updated = True
            write.writerow(req)

    return updated

# Function to delete a rejected request in the file
def deleteRequest(reqID):
    items = openFile()
    with open(filePath, mode='w', newline='') as file:
        write = csv.DictWriter(file, fieldnames=["ID", "Name", "Manufacturer", "Status"])
        write.writeheader()

        for req in items:
            if req['ID'] != reqID or req['Status'] != "Rejected":
                write.writerow(req)

# Live refresh the treeview if edits are made to the csv file. Also this is where I found how to refresh because I forgot: https://stackoverflow.com/questions/76407618/how-to-refresh-data-in-treeview-in-tkinter row is replacing i.
def refresh(tree):
    for row in tree.get_children():
        tree.delete(row)

    items = openFile()
    for req in items:
        tree.insert("", "end", values=(req["ID"], req["Name"], req["Manufacturer"], req["Status"]))


def buttonHandler(tree, action):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error!", "Please select an req to perform this action.")
        return

    reqID = tree.req(selected[0], "values")[0]
    if action == "accept":
        newStatus = "Approved"
        if updateStatus(reqID, newStatus):
            messagebox.showinfo("Success", f"Request {reqID} accepted successfully.")
    else:  # this is essentially action == "reject"
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
    columns = ("ID", "Name", "Manufacturer", "Status")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
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
    searchArea = ttk.Combobox(searchFrame, values=["ID", "Name", "Manufacturer"], state="readonly")
    searchArea.pack(side="left", padx=5)
    searchArea.current(0)

    searchText = tk.Entry(searchFrame)
    searchText.pack(side="left", padx=5)

    def searchRequests():
        field = searchArea.get()
        query = searchText.get().strip()
        if not query:
            messagebox.showwarning("Error!", "Search query cannot be empty.")
            return

        items = openFile()
        results = [req for req in items if req[field].lower() == query.lower()]

        for row in tree.get_children():
            tree.delete(row)

        for req in results:
            tree.insert("", "end", values=(req["ID"], req["Name"], req["Manufacturer"], req["Status"]))

    tk.Button(searchFrame, text="Search", command=searchRequests).pack(side="left", padx=5)

    tk.Button(root, text="Back to Main Menu", command=mainMenu).pack(pady=10)

    root.mainloop()

# This is me testing a CSV file format for the program
def create_csv():
    with open(filePath, mode='w', newline='') as file:
        write = csv.DictWriter(file, fieldnames=["ID", "Name", "Manufacturer", "Status"])
        write.writeheader()
        write.writerows([
            {"ID": "1", "Name": "Apple", "Manufacturer": "Farm", "Status": "Pending Approval"},
            {"ID": "2", "Name": "Book", "Manufacturer": "Barnes & Noble", "Status": "Pending Approval"},
            {"ID": "3", "Name": "Car", "Manufacturer": "Ford", "Status": "Pending Approval"},
        ])


# Just uncomment this line to create the test CSV, you can only do this once though or you might run in to some annoying issues
#create_csv()

# Run the GUI
main()
