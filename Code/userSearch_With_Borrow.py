'''
Title: userSearch.py
Author: Zachary Outman
    Buy/Borrow request function added by Thomas Weston
Date: 11/17/2024
'''
# Sorry for getting a little lazy and not putting any of the buttons or boxes to the left or right and where, I had no idea where to put them.
# I also didn't know what to put in the searchFrame so I just left it blank.
# Also I might display the search results vertically I just have to figure out how without breaking something.
# I also plan on adding a refresh but not sure if it's nessesary. I added it to the borrowRequest.py file so I figured I might as well add it here.

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog # added to support the borrow function
import csv
import os

filePath = "userData.csv" #You can edit the name it doesn't matter

# Function to create a favorites CSV file if it does not exist
def createFavoritesCSV():
    if not os.path.exists("favorites.csv"):
        with open("favorites.csv", "w", newline="") as file:
            write = csv.writer(file)
            write.writerow(["ID", "Name", "Producer"])

# # Function to load all items from the file
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

# Function to add an item to favorites and create or write to a csv file
def addToFavorites(item=None):
    try:
        if item is None:
            selected_item = resultsList.get(tk.ACTIVE)
            if not selected_item:
                messagebox.showwarning("Error", "Please select an item to add to favorites!")
                return
            item = dict(zip(["ID", "Name", "Producer"], [i.split(": ")[1] for i in selected_item.split(", ")]))

        fileExists = os.path.exists("favorites.csv") # This could cause an issue if the file is not found but it exists because it will make and write to a new file but I don't think that will happen
        with open("favorites.csv", "a", newline="") as file:
            write = csv.writer(file)
            if not fileExists:
                write.writerow(["ID", "Name", "Producer"])
            write.writerow([item["ID"], item["Name"], item["Producer"]])
        
        messagebox.showinfo("Favorites", "Item added to favorites!")
    except Exception as errorName:
        messagebox.showerror("Error", f"An error occurred: {errorName}")

# this is pretty much the same as the previous function but with an additional option to choose between buying an item or just borrowing it
def requestToBuy(item=None):
    try:
        if item is None:
            selected_item = resultsList.get(tk.ACTIVE)
            if not selected_item:
                messagebox.showwarning("Error", "Please select an item to request to buy or borrow")
                return
            item = dict(zip(["ID", "Name", "Producer"], [i.split(": ")[1] for i in selected_item.split(", ")]))
        fileExists = os.path.exists("BorrowList.csv") 
        with open("BorrowList.csv", "a", newline="") as file:
            write = csv.writer(file)
            if not fileExists:
                write.writerow(["ID", "Name", "Producer", "Buy or borrow"])
            write.writerow([item["ID"], item["Name"], item["Producer"], "Buy"])
        # this segment adds a copy to the user history list
        with open("UserHistory.csv", "a", newline="") as file:
            write = csv.writer(file)
            if not fileExists:
                write.writerow(["ID", "Name", "Producer",])
            write.writerow([item["ID"], item["Name"], item["Producer"]])
        messagebox.showinfo("Buy/Borrow list", "Item requested!")
    except Exception as errorName:
        messagebox.showerror("Error", f"An error occurred: {errorName}")

def requestToBorrow(item=None):
    duration = simpledialog.askstring("How long would you like to borrow this item? (please enter a # of days")
    try:
        if item is None:
            selected_item = resultsList.get(tk.ACTIVE)
            if not selected_item:
                messagebox.showwarning("Error", "Please select an item to request to buy or borrow")
                return
            item = dict(zip(["ID", "Name", "Producer"], [i.split(": ")[1] for i in selected_item.split(", ")]))
        fileExists = os.path.exists("BorrowList.csv") 
        with open("BorrowList.csv", "a", newline="") as file:
            write = csv.writer(file)
            if not fileExists:
                write.writerow(["ID", "Name", "Producer", "Buy or borrow", "Borrow duration"])
            write.writerow([item["ID"], item["Name"], item["Producer"], "Borrow", (str(duration))])
        with open("UserHistory.csv", "a", newline="") as file:
            write = csv.writer(file)
            if not fileExists:
                write.writerow(["ID", "Name", "Producer",])
            write.writerow([item["ID"], item["Name"], item["Producer"]])
        messagebox.showinfo("Buy/Borrow list", "Item requested!")
    except Exception as errorName:
        messagebox.showerror("Error", f"An error occurred: {errorName}")

# Function for the search button
def performSearch():
    search_type = searchOption.get()
    search_query = searchEntry.get()

    if not search_query:
        messagebox.showwarning("Input Error", "Please enter a search query!")
        return

    search_results = searchItems(search_type, search_query)

    resultsList.delete(0, tk.END)
    for item in search_results:
        resultsList.insert(tk.END, f'ID: {item["ID"]}, Name: {item["Name"]}, Producer: {item["Producer"]}')

    if not search_results:
        messagebox.showinfo("No Results", "No items found for your search.")

# Function to clear search and return to main menu
def clearSearch():
    searchEntry.delete(0, tk.END)
    resultsList.delete(0, tk.END)

# Main application window you can rezie it if you want but this is pretty good size
root = tk.Tk()
root.title("Regular User Search")
root.geometry("400x450")

# Search Options/ buttons for diffrent types of data
tk.Label(root, text="Search By:").pack()

searchOption = tk.StringVar(value="ID")
tk.Radiobutton(root, text="ID", variable=searchOption, value="ID").pack()
tk.Radiobutton(root, text="Name", variable=searchOption, value="Name").pack()
tk.Radiobutton(root, text="Producer", variable=searchOption, value="Producer").pack()

# Search entry
tk.Label(root, text="Enter Search Query:").pack()
searchEntry = tk.Entry(root)
searchEntry.pack()

# Here are all the cool buttons
tk.Button(root, text="Search", command=performSearch).pack()
tk.Button(root, text="Add to Favorites", command=addToFavorites).pack()
tk.Button(root, text="Clear Search", command=clearSearch).pack()
tk.Button(root, text="Main Menu", command=root.destroy).pack() #Ethan, this is where you edit the root.destroy to call your main menu function.

# Buttons added by Thomas to support the buy/borrow options
tk.Button(root, text = "Buy this item", command=requestToBuy).pack()
tk.Button(root, text = "Borrow this item", command=requestToBuy).pack()

# Search results box
resultsList = tk.Listbox(root, height=10, width=50)
resultsList.pack()

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
createCSV()

# Run the Application
root.mainloop()
