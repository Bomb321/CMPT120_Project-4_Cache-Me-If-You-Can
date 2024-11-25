'''
Title: userSearch.py
Author: Zachary Outman
Date: 11/17/2024
'''
# Sorry for getting a little lazy and not putting any of the buttons or boxes to the left or right and where, I had no idea where to put them.
# I also didn't know what to put in the searchFrame so I just left it blank.
# Also I might display the search results vertically I just have to figure out how without breaking something.
# I also plan on adding a refresh but not sure if it's nessesary. I added it to the borrowRequest.py file so I figured I might as well add it here.

#Added Refresh button, search results vertically instad of horizontally, and have a pop up for when adding to favorites.
#Also made the GUI much better and a dynamic search bar that updates the search results as you type just like adminViewBorrowRequest.py

import tkinter as tk
from tkinter import messagebox
import csv
import os
from tkinter import ttk

filePath = "userData.csv" #You can edit the name it doesn't matter

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
    return [item for item in items if item[search_type].lower() == search_query.lower()]

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
            item = {"ID": item_values[0], "Name": item_values[1], "Producer": item_values[2]}

        fileExists = os.path.exists("favorites.csv")
        with open("favorites.csv", "a", newline="") as file:
            write = csv.writer(file)
            if not fileExists:
                write.writerow(["ID", "Name", "Producer"])
            write.writerow([item["ID"], item["Name"], item["Producer"]])
        
        messagebox.showinfo("Favorites", "Item added to favorites successfully!")
    except Exception as errorName:
        messagebox.showerror("Error", f"An error occurred: {errorName}")

# Function to load all users from csv
def loadAllUsers():
    items = openFile()
    for item in items:
        tree.insert("", tk.END, values=(item["ID"], item["Name"], item["Producer"]))

# Function for the search button
def performSearch(event=None):
    search_type = searchOption.get()
    search_query = searchEntry.get().strip()

    #This is because a issue happened that when the search was blank no items would show up
    if not search_query:
        loadAllUsers()  
        return

    search_results = searchItems(search_type, search_query)

    for row in tree.get_children():
        tree.delete(row)
    for item in search_results:
        tree.insert("", tk.END, values=(item["ID"], item["Name"], item["Producer"]))

# Function to clear search and return to main menu
def clearSearch():
    searchEntry.delete(0, tk.END)
    for row in tree.get_children():
        tree.delete(row)
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

searchOption = tk.StringVar(value="ID")
tk.Radiobutton(searchFrame, text="ID", variable=searchOption, value="ID").grid(row=0, column=1, padx=5)
tk.Radiobutton(searchFrame, text="Name", variable=searchOption, value="Name").grid(row=0, column=2, padx=5)
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
tk.Button(buttonFrame, text="Main Menu", command=root.destroy).grid(row=0, column=3, padx=5)

# Search results treeview
treeFrame = tk.Frame(root)
treeFrame.pack(pady=10, fill=tk.BOTH, expand=False)  

tree = ttk.Treeview(treeFrame, columns=("ID", "Name", "Producer"), show="headings", height=10) 
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Producer", text="Producer")
tree.pack(side="left", fill=tk.BOTH, padx=10, pady=10) 

scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Load all users for treeview
loadAllUsers()

# This is me testing a CSV file format for the program
def createCSV():
    with open(filePath, mode='w', newline='') as file:
        write = csv.DictWriter(file, fieldnames=["ID", "Name", "Producer"])
        write.writeheader()
        write.writerows([
            {"ID": "1", "Name": "Apple", "Producer": "Farm"},
            {"ID": "2", "Name": "Book", "Producer": "Barnes & Noble"},
            {"ID": "3", "Name": "Car", "Producer": "Ford"},
        ])
# Just uncomment this line to create the test CSV, you can only do this once though or you might run in to some annoying issues
#createCSV()

# Run the Application
root.mainloop()
