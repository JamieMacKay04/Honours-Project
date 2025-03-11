import requests
from datetime import datetime, timedelta

# Function to print 7-day weather forecast
def print_weather_forecast():
    api_key = "DDuIZsg03kGXpOLtW9xo1QYHnEcfTWUu"
    location = "55.8652,-4.2576"
    endpoint = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}&timesteps=1d&units=metric"

    response = requests.get(endpoint).json()

    if 'timelines' not in response or 'daily' not in response['timelines']:
        print("⚠️ Error fetching weather data.")
        print(response)  # Print full response for debugging
        return

    print("📅 7-Day Weather Forecast for Glasgow:")
    for entry in response['timelines']['daily']:
        date = entry['time'].split('T')[0]
        temperature = entry['values']['temperatureAvg']
        rainfall = entry['values'].get('precipitationIntensityAvg', 0)
        print(f"{date} | 🌡️ {temperature}°C | 🌧️ {rainfall}mm")

# Run the weather forecast display function
print_weather_forecast()