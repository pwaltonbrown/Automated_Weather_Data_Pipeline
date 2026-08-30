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
    try:
        # Make a GET request to the CSV file
        df = pd.read_csv(CSV_URL)
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Check if the date column exists
        if DATE_COlUMN not in df.columns:
            raise ValueError(f"Column '{DATE_COlUMN}' not found. Available columns: {list(df.columns)}")
            
        # Strip commas from date column
        df[DATE_COlUMN] = df[DATE_COlUMN].astype(str).str.strip().str.rstrip(",")
        
        # Convert the date column to datetime
        df[DATE_COlUMN] = pd.to_datetime(df[DATE_COlUMN], format="%Y-%m-%d %H:%M:%S")
        
        # Drop rows with missing date
        df = df.dropna(subset=[DATE_COlUMN])
        return df
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return None

# filters data by the selected date
def show_day_data():
    # Get the selected date
    selected_date = cal.get_date()
    
    # Fetch data
    df = fetch_data()
    if df is None:
        return

    # FIX 1: Extract just the pure date (.dt.date) to match the cal.get_date() structure
    filtered_df = df[df[DATE_COlUMN].dt.date == selected_date]
    
    # Check if filtered DataFrame is empty
    if filtered_df.empty:
        messagebox.showinfo("No Data", f"No data found for the selected date: {selected_date}")
        return
        
    display_df = filtered_df.copy()
    # FIX 2: Corrected typo from .dt.srtftime to .dt.strftime
    display_df[DATE_COlUMN] = display_df[DATE_COlUMN].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # create a popup window for the table
    popup = tk.Toplevel(root)
    popup.title("Weather Data for " + selected_date.strftime("%Y-%m-%d"))
    popup.geometry("700x400")
    
    # create a frame to hold the table
    frame = tk.Frame(popup)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # create the table
    columns = list(display_df.columns)
    table = ttk.Treeview(frame, columns=columns, show="headings")
    
    # add the table to the frame
    table.grid(row=0, column=0, sticky="nsew")
    
    # create scrollbars
    vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
    
    # pack scrollbars
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    
    # configure the table scroll connection
    table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # configure the frame weighting
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    
    # add columns and headings to the table
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=130, anchor="center")
        
    # add rows to the table using the properly formatted text values
    for _, row in display_df.iterrows():
        table.insert("", "end", values=list(row))

# create the main window
root = tk.Tk()
root.title("Github Raleigh NC Weather Data Viewer")
root.geometry("350x200")
root.eval('tk::PlaceWindow . center')

label = ttk.Label(root, text="Select a date: ", font=("Arial", 12))
label.pack(pady=15)

# create a date entry widget
cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
cal.pack(pady=10)

# submit button
btn = tk.Button(root, text="Fetch day's data", command=show_day_data, bg="green", fg="white", font=("Arial", 10, "bold"))
btn.pack(pady=15)

# run the main loop
root.mainloop()
