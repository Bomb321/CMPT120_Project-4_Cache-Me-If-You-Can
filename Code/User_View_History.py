'''
User view history
Thomas Weston
11/15/2024
'''

import csv
import os
import tkinter as tk
from tkinter import ttk
 
# tysm Zach for the tkiner tutorials c:

# csv file writing for testing purposes -- in the main code this will occour in the buy/borrow function. Will disable before github upload

filename = "UserHistory.csv"

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    fields = ['Product ID','Product Name','Product Producer']

    writer.writerow(fields)
    writer.writerow(["12345", "Hamburger", "McDonalds"])
    writer.writerow(["54321", "Book", "ABC Inc"])
    writer.writerow(["24601", "CD", "XYZ Corp"])


# heres where the actual code that matters starts
root = tk.Tk()
root.title("View History")

root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)


def ShowUserHistory():
    filename = "UserHistory.csv"

# The Buy/Borrow list will be repeated in this list, but unlike the buy/borrow list, this will not delete files after the request is approved or denied.


    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        #fields=next(csvreader)

        for row in csvreader:
            HistList.insert(tk.END, row)





# tree stuff
info_tree = ttk.Treeview(root)
info_tree['columns'] = fields

for col in fields:
    info_tree.column(col, width=100)
    info_tree.heading(col, text=col)

for row in csvreader:
    info_tree.insert("", "end", values=row)
    

info_tree.heading("#0", text="Label",)
info_tree.heading("ID", text="Product ID",)
info_tree.heading("Name", text="Product Name",)
info_tree.heading("Producer", text="Product Producer",)


info_tree.insert(parent=" ", index="end", iid=0, text="Parent", values=("1", "Burger", "McDonalds"))

info_tree.pack(pady=20)





def mainMenu():
    root.destroy()

#obviously this will be replaced with the actual main menu function 


# buttons and stuff
btn_show = tk.Button(root, text="Show History", command= ShowUserHistory)
btn_show.grid(row=0, column=0)

HistList= tk.Listbox(root)
HistList.grid(row=1, column=0, columnspan=20, sticky = "ew")

btn_return = tk.Button(root, text="Return to Main Menu", command= mainMenu) #temp command for testing purposes
btn_return.grid(row=0, column=1)

root.mainloop()

