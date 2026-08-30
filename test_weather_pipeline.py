# Name: test_weather_pipeline.py
# Description: This is a program to test weather_pipeline.py url and params are correct and returns early on failed api response
# Author: Patrick Brown
# Date: 6/7/2026


# Import libraries
import unittest
from unittest.mock import patch, Mock
import weather_pipeline

# Test the run_pipeline function
class WeatherPipelineTests(unittest.TestCase):
    
    def tearDown(self):
        """Cleans up leftover files created by un-mocked pandas functions."""
        if os.path.exists("weather_history.csv"):
            os.remove("weather_history.csv")
    
    @patch("weather_pipeline.os.path.exists", return_value=False)
    @patch("pandas.DataFrame.to_csv")
    @patch("requests.get")
    def test_run_pipeline_builds_request_with_base_url_and_params(self, mock_get, _mock_to_csv, _mock_exists):
        
        # Mock the API response
        mock_response = Mock(status_code=200)
        
        # Mock the JSON response
        mock_response.json.return_value = {
            "name": "Raleigh",
            "main": {"temp": 75, "humidity": 40},
            "weather": [{"description": "clear sky"}],
        }
        
        # Mock the requests.get function
        mock_get.return_value = mock_response

        # Call the run_pipeline function
        weather_pipeline.run_pipeline()
            
        # this is to Make sure there's a ? before the first parameter
        expected_url = f"https://api.openweathermap.org/data/2.5/weather?q={weather_pipeline.CITY.replace(',', '%2C')}&appid={weather_pipeline.API_KEY}&units=imperial"

        # Assert that requests.get was called with the exact literal string layout
        mock_get.assert_called_once_with(expected_url)

    # Test the run_pipeline function
    @patch("weather_pipeline.os.path.exists", return_value=False)
    @patch("pandas.DataFrame.to_csv")
    @patch("requests.get")
    def test_run_pipeline_returns_early_on_failed_api_response(self, mock_get, mock_to_csv, _mock_exists):
        mock_get.return_value = Mock(status_code=500, text="server error")

        # Call the run_pipeline function
        weather_pipeline.run_pipeline()

        # Assert that the to_csv function was not called
        mock_to_csv.assert_not_called()

# Run the tests
if __name__ == "__main__":
    unittest.main()
