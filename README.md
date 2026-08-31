
# Automated Weather Data Pipeline

My degree focused heavily on traditional software development, so I wanted to teach myself cloud-native data pipelines. I used Al tools to rapidly prototype a serverless ETL pipeline, which allowed me to focus on understanding system architecture, event-driven triggers, and data validation constraints.

This automated Python pipeline fetches daily weather data from OpenWeatherMap, organizes it into a clean format, and appends it to a historical CSV ledger using GitHub Actions.

## 🚀 Features

* **Automated Data Retrieval**: Fetches high/low temperatures, humidity, and forecasts daily.
* **Hands-Free Automation**: A GitHub Actions workflow runs the script 6 times a day.
* **Self-Committing Ledger**: Automatically commits and pushes new data directly to the repository.
* **Robust Testing**: Built-in unit tests verify API parameters and handle failures gracefully.

## 🛠️ Tech Stack & Prerequisites

This program requires **Python 3.x** and the following packages:

* `requests` - For API interaction
* `pandas` - For data manipulation
* `pyarrow` - Backend storage engine for Pandas
* `unittest` - For running the test suite

Install the dependencies using pip:

```bash
pip install requests pandas pyarrow
```

## 📂 File Structure

* `requirements.txt`: Contains the names and version numbers of the required python packets needed.
* `weather_pipeline.py`: The core script that fetches and structures the weather data.
* `weather_history.csv`: The rolling ledger storing all historical weather records.
* `test_weather_pipeline.py`: Unit tests ensuring URL accuracy and API error handling.
* `user_access_program.py`: The program script that allows users to access the weater_history.csv data from their home computer without going to GitHub.
* `.github/workflows/data_pipeline.yml`: The GitHub Actions workflow automating the execution.

## ⚙️ Configuration

1. Sign up for a free API key at [openweathermap.org](https://openweathermap.org).
2. Add your API key to your GitHub repository secrets as `OPENWEATHER_API_KEY`.

## 🧪 Running Tests

The workflow file data_pipline.yml runs validation of the API URL parameters and error handling before running the actual program file weather_pipline.py using test_weather_pipline.py every time that the workflow runs its scheduled data pull 6 times a day.

## User Program

The user_access_program.py file can be downloaded on to your computer. When run with all the required libraries from requierments.txt installed, and Wi-Fi enabled, you can access the weather_history.csv file and check the weather for any day the pipeline has a record for.
