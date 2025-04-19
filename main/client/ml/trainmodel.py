import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input,Dense
from datetime import datetime, timedelta
import requests  # For fetching weather data
from pymongo import MongoClient
import os
import subprocess
os.environ["PYTHONIOENCODING"] = "utf-8"

dir_path = os.path.dirname(os.path.realpath(__file__))

def connect_to_mongo():
    MONGO_URI = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_URI)
    db = client['mydatabase']
    return db['stockitems']

def get_current_stock(item_name, category):
    collection = connect_to_mongo()
    item = collection.find_one({"Item Name": item_name})
    if item:
        quantity = item.get('quantity', 0)
        if category.strip().lower() == 'spirits':
            quantity = quantity / 1000  # Convert ml back to bottles for spirits
        return int(quantity)  # Ensure it's an integer
    return 0  # Default if no item is found

def get_season():
    month = datetime.now().month
    if month in (3, 4, 5):
        return 'Spring'
    elif month in (6, 7, 8):
        return 'Summer'
    elif month in (9, 10, 11):
        return 'Autumn'
    else:
        return 'Winter'


# Function to fetch weather data
def get_weather_forecast():
    api_key = "DDuIZsg03kGXpOLtW9xo1QYHnEcfTWUu"
    location = "55.8652,-4.2576"
    endpoint = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}&timesteps=1d&units=metric"
    response = requests.get(endpoint).json()
    if 'timelines' not in response or 'daily' not in response['timelines']:
        print(" Error fetching weather data.")
        return 12, 0  # Default values if API fails
    forecast_data = response['timelines']['daily']
    weekday_weight = {0: 0.7, 1: 0.7, 2: 0.7, 3: 0.7, 4: 1.3, 5: 1.3, 6: 1}  # Weighting system for weekdays
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
    print(f" Weighted Temperature: {avg_temp}°C |  Weighted Rainfall: {avg_rainfall}mm")
    return avg_temp, avg_rainfall

dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path, 'stockOrders.csv')
df = pd.read_csv(csv_path)


df = pd.get_dummies(df, columns=["Season"])
X = df[["Week", "Projected Covers", "Stock Left"] + list(df.filter(like="Season_").columns)]
y = df["Ordered Stock"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = Sequential([
    Input(shape=(X_train.shape[1],)),  
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
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

output_path = os.path.join(dir_path, 'newOrder.csv')
output.to_csv(output_path, index=False)

# Predict next week's stock order
last_week = df[df["Week"] == df["Week"].max()]
next_week = last_week.copy()
next_week["Week"] = last_week["Week"] + 1  # Increment week
temp, rain = get_weather_forecast()
next_week['Projected Covers'] = last_week['Projected Covers'].mean() * (1.2 if temp >= 16 and rain == 0 else 0.8 if rain > 5 else 1)
X_next_week = scaler.transform(next_week[X.columns])
predicted_stock = model.predict(X_next_week)
next_week["Ordered Stock"] = [math.ceil(val[0]) for val in predicted_stock]

# Add 'Season' column dynamically
next_week["Season"] = get_season()

# Fetch and adjust Stock Left, converting ml to bottles for spirits
next_week["Stock Left"] = next_week.apply(lambda row: get_current_stock(row["Item Name"], row["Category"]), axis=1)

# Now, select only the columns you need and save to new CSV
output_columns = ["Week", "Item Name", "Category", "Ordered Stock", "Projected Covers", "Stock Left", "Season"]
final_output = next_week[output_columns]
stock_orders_path = os.path.join(dir_path, 'stockOrders.csv')
final_output.to_csv(stock_orders_path, mode='a', header=False, index=False)

output_path = os.path.join(dir_path, 'newOrder.csv')
print(f"Saving newOrder.csv to: {output_path}")  # Debugging Step
output.to_csv(output_path, index=False)

