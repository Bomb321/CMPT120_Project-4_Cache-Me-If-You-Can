'''
User_View_History
Version 2
Thomas Weston
11/17/2024
''' 

import csv
import tkinter as tk
from tkinter import ttk


# writing to file for testing purposes
filename = "UserHistory.csv"

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    fields = ['ID','Name','Producer']

    writer.writerow(["1", "Hamburger", "McDonalds"])
    writer.writerow(["2", "Book", "ABC Inc"])
    writer.writerow(["3", "CD", "XYZ Corp"])



root = tk.Tk()
root.title("User view history")
root.geometry("500x500")

tree = ttk.Treeview(root)

tree['columns'] = (fields)
# columns
tree.column("#0", width=0, minwidth=0)
tree.column("ID", anchor="w", width=120, minwidth=25)
tree.column("Name", anchor="center", width=120, minwidth=25)
tree.column("Producer", anchor="w", width=120, minwidth=25)

#headings
tree.heading("#0", text="", anchor="w")
tree.heading("ID", text="Product ID", anchor="w")
tree.heading("Name", text="Product Name", anchor="center")
tree.heading("Producer", text="Product Producer", anchor="w")

# reading the file and inputting data
with open(filename, 'r',) as file:
    reader = csv.reader(file)
    for row in reader:
        tree.insert("", "end", values=(row))

tree.grid(row=0, column=0)

#buttons and functions for returning to main menu
def mainMenu():
    root.destroy()

#obviously this will redirect in the full version and just terminate.

btn_return = tk.Button(root, text="Return to Main Menu", command= mainMenu) #temp command for testing purposes
btn_return.grid(row=1, column=0)

root.mainloop()
