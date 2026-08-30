# name: user_access_program.py
# description: This is a program that will allow a user to search for a date and view its forcast data from their home computer.
# Author: patrick brown
# Date: 8/30/2026

# import libraries
import sys
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
        # Make a GET request to the CSV file
        df = pd.read_csv(CSV_URL)

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Check if the date column exists
        if DATE_COlUMN not in df.columns:

            # Show an error message
            raise ValueError(f"Column '{DATE_COlUMN}' not found. avalable columns: {list(df.columns)}")

        # Strip commas from date column
        df[DATE_COlUMN] = df[DATE_COlUMN].astype(str).str.strip().str.rstrip(",")

        # Convert the date column to datetime
        df[DATE_COlUMN] = pd.to_datetime(df[DATE_COlUMN], format="%Y-%m-%d %H:%M:%S")

        # Drop rows with missing date
        df = df.dropna(subset=[DATE_COlUMN])

        # Return the DataFrame
        return df

    # Handle any exceptions
   except requests.exceptions.RequestException as e:

        # Show an error message
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

        # Return None
        return None

# filters data by the selected date
def show_day_data():

    # Get the selected date
    selected_date = cal.get_date()

    # Fetch data
    df = fetch_data()

    # Check if data is available
    if df is None:

        # Show an error message
        messagebox.showerror("Error", "Failed to fetch data.")

        # Return
        return

    # Filter the DataFrame
    filtered_df = df[df[DATE_COlUMN] == selected_date]

    # Check if filtered DataFrame is empty
    if filtered_df.empty:

        # Show an error message
        messagebox.showinfo("No Data", "No data found for the selected date.")

        # Return
        return

    display_df = filtered_df.copy()
    display_df[DATE_COlUMN] = display_df[DATE_COlUMN].dt.srtftime("%Y-%m-%d %H:%M:%S")

    # create a popup window for the table
    popup = tk.Toplevel(root)

    # set the title of the popup window
    popup.title("Weather Data for " + selected_date.strftime("%Y-%m-%d"))

    # set the size of the popup window
    popup.geometry("700x400")

    # create a frame to hold the table
    frame = tk.Frame(popup)

    # pack the frame into the popup window
    frame.pack(fill= tk.BOTH, expand=True, padx=10, pady=10)

    # create the table
    columns = list(display_df.columns)
    table = ttk.Treeview(frame, columns=columns, show="headings")


    # add the table to the frame
    table.grid(row=0, column=0, sticky="nsew")

    # create the scrollbar
    vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)

    # configure the table
    table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # configure the frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # configure the table
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

# create the main window
root = tk.Tk()

# set the title of the window
root.title("Github Raleigh NC Weather Data Viewer")

# set the size of the window
root.geometry("350x200")

# center the window
root.eval('tk::PlaceWindow . center')

label = ttk.Label(root, text = "select a date: ", font=("Arial", 12)).pack(pady=15)

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
