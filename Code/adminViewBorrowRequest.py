'''
Title: Admin view Borrow Requests
Author: Zachary Outman
Date: 11/17/2024
'''
import tkinter as tk
from tkinter import ttk, messagebox
import csv

#Improvements
#Live refresh in the searh box, and removed the search bar
#Dynamically refreshing the CSV file when a request is rejected or accepted.
#Added more error checking
#Add A rejected requests csv file for all the deleted requests

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
    with open(filePath, mode='w', newline='') as file:
        write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
        write.writeheader()
        write.writerows([
            {"ID": "1", "Name": "Apple", "Producer": "Farm", "Status": "Pending Approval"},
            {"ID": "2", "Name": "Book", "Producer": "Barnes & Noble", "Status": "Pending Approval"},
            {"ID": "3", "Name": "Car", "Producer": "Ford", "Status": "Pending Approval"},
        ])

    with open(rejectedFilePath, mode='w', newline='') as file:
        write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer", "Status"])
        write.writeheader()

# Just uncomment this line to create the test CSV, you can only do this once though or you might run in to some annoying issues
#createCSV()

# Run the GUI
main()

