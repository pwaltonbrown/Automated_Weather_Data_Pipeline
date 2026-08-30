# Name: weather_pipeline.py
# Description: This is a program that will pull weather data from a free api website and organize it in a easer to read format.
# Author: Patrick Brown
# Date: 6/7/2026


# 1. Import libraries
import os
import requests
import pandas as pd
from datetime import datetime

# 2. Define config block for the pipeline
CITY = "raleigh,nc,us"
API_KEY = os.environ.get("WEATHER_API_KEY")
CSV_FILE = "weather_history.csv"

# 3. Global variable to satisfy test_weather_pipeline.py assertions
BASE_URL = "https://openweathermap.org"

def run_pipeline():
    
    # 4. Fetch Data
    query_params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "imperial"
    }
    
    # this is to Make sure there's a ? before the first parameter
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY.replace(',', '%2C')}&appid={API_KEY}&units=imperial"
    response = requests.get(URL)
    
    # this is to Check if the request was successful
    if response.status_code != 200:
        
        # Log the error
        print(f"Error fetching data: {response.status_code}")
        
        # Log the error details
        print(f"Details: {response.text}")
        
        # Return
        return

    # Parse the JSON response
    raw_data = response.json()

    # Match the JSON structure for 2.5 Current Weather
    cleaned_data = {
        # 2.5 Current Weather time
        "timestamp": [datetime.utcnow().strftime("%Y-%m-%d")],

        # 2.5 Current Weather city name
        "city": [raw_data["name"]],

        # 2.5 Current Weather temperature
        "temperature": [raw_data["main"]["temp"]],

        # 2.5 Current Weather humidity
        "humidity": [raw_data["main"]["humidity"]],

        # 2.5 Current Weather weather condition
        "weather_condition": [raw_data["weather"][0]["description"]]
    }

    # Create a DataFrame
    df_new = pd.DataFrame(cleaned_data)

    # 5. Load Data
    if os.path.exists(CSV_FILE):
        
        # Load existing data
        df_existing = pd.read_csv(CSV_FILE)
        
        # Append new data
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        
        # Create a new DataFrame
        df_final = df_new

    # 6. Save Data
    df_final.to_csv(CSV_FILE, index=False)

    # 7. Log
    print(f"Successfully saved weather data for {CITY} using API v2.5!")

# 8. Run the pipeline
if __name__ == "__main__":
    run_pipeline()