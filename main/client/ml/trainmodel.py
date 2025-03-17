import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from datetime import datetime, timedelta
import requests  # For fetching weather data

# Function to fetch weather data
def get_weather_forecast():
    api_key = "DDuIZsg03kGXpOLtW9xo1QYHnEcfTWUu"
    location = "55.8652,-4.2576"
    endpoint = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}&timesteps=1d&units=metric"
    response = requests.get(endpoint).json()
    if 'timelines' not in response or 'daily' not in response['timelines']:
        print("⚠️ Error fetching weather data.")
        return 12, 0  # Default values if API fails
    forecast_data = response['timelines']['daily']
    weekday_weight = {0: 0.7, 1: 0.7, 2: 0.7, 3: 0.7, 4: 0.7, 5: 1.3, 6: 1.3}  # Weighting system for weekdays
    weighted_temp = 0
    weighted_rainfall = 0
    for entry in forecast_data:
        date = datetime.strptime(entry['time'].split('T')[0], "%Y-%m-%d")
        weekday = date.weekday()
        temp = entry['values']['temperatureAvg']
        rain = entry['values'].get('precipitationIntensityAvg', 0)
        weighted_temp += temp * weekday_weight[weekday]
        weighted_rainfall += rain * weekday_weight[weekday]
    avg_temp = weighted_temp / sum(weekday_weight.values())
    avg_rainfall = weighted_rainfall / sum(weekday_weight.values())
    print(f"🌡️ Weighted Temperature: {avg_temp}°C | 🌧️ Weighted Rainfall: {avg_rainfall}mm")
    return avg_temp, avg_rainfall

# Load dataset
df = pd.read_csv("stockOrders.csv")
df = pd.get_dummies(df, columns=["Season"])
X = df[["Week", "Projected Covers", "Stock Left"] + list(df.filter(like="Season_").columns)]
y = df["Ordered Stock"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build and train model
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(1)
])
model.compile(optimizer="adam", loss="mse")
model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=1)

# Predict next week's stock order
last_week = df[df["Week"] == df["Week"].max()]
next_week = last_week.copy()
next_week["Week"] += 1
temp, rain = get_weather_forecast()
next_week['Projected Covers'] = last_week['Projected Covers'].mean() * (1.2 if temp >= 16 and rain == 0 else 0.8 if rain > 5 else 1)
X_next_week = scaler.transform(next_week[X.columns])
predicted_stock = model.predict(X_next_week)
next_week["Ordered Stock"] = [math.ceil(val[0]) for val in predicted_stock]

# Select columns to save
output = next_week[["Item Name", "Category", "Ordered Stock"]]

# Save to new CSV
output.to_csv('newOrder.csv', index=False)
