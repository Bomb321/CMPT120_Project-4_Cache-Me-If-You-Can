'''
Title: View Favorite List
Author: Ryan Taylor
Date: 11/17/2024
'''

# import packages
import csv
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

filename= 'Favorites.csv'

# create the csv file for testing & used the same data as group
def createCSV():
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        fields = ['Product ID','Product Name','Product Producer']
        writer.writerow(fields)
        writer.writerow(["12345", "Hamburger", "McDonalds"])
        writer.writerow(["54321", "Book", "ABC Inc"])
        writer.writerow(["24601", "CD", "XYZ Corp"])

# GUI setup
root= tk.Tk()
root.title("View Favorites")
root.geometry("700x400")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

# global treeview widget to use for mulitple fucntions
info_tree = ttk.Treeview(root, columns=("Product ID", "Product Name", "Product Producer"), show="headings")

# user friendly enhancements
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

frame_treeview = tk.Frame(root)
frame_treeview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# helper function that clears the treeview
def clearTreeview():
    for item in info_tree.get_children():
        info_tree.delete(item)

def viewFavorites():
    # configure treeview widget and columns
    info_tree.grid(row=2, column=0, columnspan=3, sticky="ew")
    info_tree.heading("Product ID", text="Product ID", command=lambda: sortFavorites("Product ID"))
    info_tree.column("Product ID", width=100)
    info_tree.heading("Product Name", text="Product Name", command=lambda: sortFavorites("Product Name"))
    info_tree.column("Product Name", width=150)
    info_tree.heading("Product Producer", text="Product Producer", command=lambda: sortFavorites("Product Producer"))
    info_tree.column("Product Producer", width=150)
    clearTreeview()
    # read the csv and add to the treeview
    with open(filename, mode="r") as csvfile:
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
    info_tree.delete(select_item)
    # update csv file
    with open(filename, mode='r') as csvfile:
        rows = list(csv.reader(csvfile))
    #filter out row to be removed
    rows= [row for row in rows if row != list(select_values)]
    #rewrite csv file
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
        
    messagebox.showinfo("Success", f"Removed {select_values[1]} successfully!")

def searchFavorites():
    search_query = search_entry.get().lower()
    if not search_query:
        messagebox.showwarning("Empty Search", "Please enter a search term.")
        return
    clearTreeview()
    # read the csv file and display matching rows
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if any(search_query in cell.lower() for cell in row):
                info_tree.insert("", tk.END, values=row)

# global variable to track sorting state
sort_order = {"Product ID": False, "Product Name": False, "Product Producer": False}

def sortFavorites(column):
    data = [info_tree.item(child, "values") for child in info_tree.get_children()]
    column_index = ["Product ID", "Product Name", "Product Producer"].index(column)
    reverse = sort_order[column]
    sort_order[column] = not reverse  
    if column == "Product ID":
        data.sort(key=lambda x: int(x[column_index]) if x[column_index].isdigit() else 0, reverse=reverse)
    else:
        data.sort(key=lambda x: x[column_index].lower(), reverse=reverse)
    clearTreeview()
    for row in data:
        info_tree.insert("", tk.END, values=row)
    
# function to main menu but this is a place holder
def mainMenu():
    root.destroy()

# widgets
search_label = tk.Label(frame_buttons, text="Search Products:")
search_label.grid(row=1, column=0, padx=10, pady=5)

search_entry = tk.Entry(frame_buttons, width=30)
search_entry.grid(row=1, column=1, padx=10, pady=5)

# buttons
btn_show = tk.Button(frame_buttons, text="View Favorites", command=viewFavorites)
btn_show.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

btn_search = tk.Button(frame_buttons, text="Search", command=searchFavorites)
btn_search.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

btn_remove = tk.Button(frame_buttons, text="Remove Selected Product", command=removeFavorites)
btn_remove.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

btn_return = tk.Button(frame_buttons, text="Return to Main Menu", command=mainMenu)  # Main menu placeholder
btn_return.grid(row=0, column=2, pady=10, padx=10, sticky="ew")

# initialize csv and run the GUI
createCSV()
root.mainloop()
