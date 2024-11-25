import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

# Define the CSV file names
PRODUCT_CSV = 'products.csv'
HISTORY_CSV = 'product_history.csv'

# Ensure the CSV file and history file exist with proper headers if not already there
def makecsv():
    if not os.path.exists(PRODUCT_CSV):
        with open(PRODUCT_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Product ID', 'Producer'])  # Write headers

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
