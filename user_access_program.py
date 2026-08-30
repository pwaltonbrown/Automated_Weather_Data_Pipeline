# name: user_access_program.py
# description: This is a program that will allow a user to search for a date and view its forcast data from their home computer.
# Author: patrick brown
# Date: 8/30/2026

# import libraries
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from io import StringIO
from tkcalendar import DateEntry

# Global variables

# use raw github url
CSV_URL = "https://github.com/pwaltonbrown/Automated_Weather_Data_Pipeline/blob/main/weather_history.csv?raw=true"

# Column name containing the date
DATE_COlUMN = "timestamp"

# downloads the most recent CSV data from GitHub
def fetch_data():
    # Fetch data from CSV
   try:
        # Send a GET request to the CSV URL
        response = requests.get(CSV_URL)

        # Check if the request was successful
        response.raise_for_status()

        # Read the CSV data into a pandas DataFrame
        return pd.read_csv(StringIO(response.text))

    # Handle any exceptions
   except requests.exceptions.RequestException as e:

        # Show an error message
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

        # Return None
        return None

# filters data by the selected date
def show_day_data():

    # Fetch data
    df = fetch_data()

    # Check if data is available
    if df is None:

        # Show an error message
        messagebox.showerror("Error", "Failed to fetch data.")

        # Return
        return

    # get the selected date
    selcted_date = cal.get_date()

    # Filter the DataFrame
    filtered_df = df[df[DATE_COlUMN] == selcted_date]

    # Check if filtered DataFrame is empty
    if filtered_df.empty:

        # Show an error message
        messagebox.showinfo("No Data", "No data found for the selected date.")

        # Return
        return

    # create a popup window for the table
    popup = tk.Toplevel(root)

    # set the title of the popup window
    popup.title("Weather Data for " + selcted_date)

    # create a table to display the filtered data
    table = ttk.Treeview(popup, columns=list(filtered_df.columns), show="headings")

    # add columns to the table
    for col in filtered_df.columns:

        # add a heading to the column
        table.heading(col, text=col)

        # set the width of the column
        table.column(col, width=100, anchor="center")

    # add rows to the table
    for _, row in filtered_df.iterrows():

        # add a row to the table
        table.insert("", "end", values=list(row))

    # create a scrollbar
    vsb = ttk.Scrollbar(popup, orient="vertical", command=table.yview)

    # configure the table
    table.configure(yscrollcommand=vsb.set)

    # pack the table into the popup window
    table.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # pack the scrollbar into the popup window
    vsb.pack(side="right", fill="y",pady=10)

# create the main window
root = tk.Tk()

# set the title of the window
root.title("Github Raleigh NC Weather Data Viewer")

# set the size of the window
root.geometry("350x200")

tk.label(root, text = "select a date: ", font=("Arial", 12)).pack(pady=10)

# create a date entry widget
cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')

# pack the date entry widget
cal.pack(pady=10)

# submit button
btn = tk.Button(root, text="Fetch day's data", command=show_day_data, bg="green", fg="white", font = ("Arial", 10, "bold"))

# pack the button
btn.pack(pady=15)

# run the main loop
root.mainloop()
