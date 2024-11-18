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


filename= 'Favorites.csv'

# create the csv file for testing & used the same data
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
root.geometry("400x300")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

def viewFavorites():
    # create treeview widget
    info_tree = ttk.Treeview(root, columns=("Product ID", "Product Name", "Product Producer"), show="headings")
    info_tree.grid(row=1, column=0, columnspan=2, sticky="ew")
    # columns and headings
    info_tree.heading("Product ID", text="Product ID")
    info_tree.column("Product ID", width=100)
    info_tree.heading("Product Name", text="Product Name")
    info_tree.column("Product Name", width=150)
    info_tree.heading("Product Producer", text="Product Producer")
    info_tree.column("Product Producer", width=150)
    # read the csv and add into the treeview
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            info_tree.insert("",tk.END,values=row)

# function to main menu but this is a place holder
def mainMenu():
    root.destroy()

btn_show = tk.Button(root, text="View Favorites", command= viewFavorites)
btn_show.grid(row=0, column=0, pady=10, padx=10)

btn_return = tk.Button(root, text="Return to Main Menu", command= mainMenu) # main menu placeholder
btn_return.grid(row=0, column=1, pady=10, padx=10)

createCSV()

root.mainloop()
