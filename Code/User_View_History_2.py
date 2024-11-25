'''
User_View_History
Version 2.5

11/23/2024
''' 

import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# writing to file for testing purposes 

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



#this function will loop back to the main menu
def mainMenu():
    root.destroy()
#obviously this will change in the full version




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

# this line is for debugging -- uncomment it if you need to. 
#    print(RIndex) 

    messagebox.showinfo("History", "Item Deleted! Refresh List if change is not present")




tk.Label(root,text="Press refresh to see values.").grid(row=1, column=0)

btn_refresh = tk.Button(root, text="Refresh List", command= ListRefresh)
btn_refresh.grid(row=2, column=0)

btn_return = tk.Button(root, text="Return to Main Menu", command= mainMenu)
btn_return.grid(row=3, column=0)

btn_delete = tk.Button(root, text="Delete item from history", command= delHistory)
btn_delete.grid(row=4, column=0)

root.mainloop()
