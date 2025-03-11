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

    # Weight heavier for Fri-Sun, lighter for Mon-Thu
    weekday_weight = {0: 0.7, 1: 0.7, 2: 0.7, 3: 0.7, 4: 0.7, 5: 1.3, 6: 1.3}  # Mon-Thu = 0.7, Fri-Sun = 1.3

    weighted_temp = 0
    weighted_rainfall = 0

    for entry in forecast_data:
        date = datetime.strptime(entry['time'].split('T')[0], "%Y-%m-%d")
        weekday = date.weekday()  # 0 = Monday, 6 = Sunday
        temp = entry['values']['temperatureAvg']
        rain = entry['values'].get('precipitationIntensityAvg', 0)

        weighted_temp += temp * weekday_weight[weekday]
        weighted_rainfall += rain * weekday_weight[weekday]

    # Normalize the weighted values
    total_weight = sum(weekday_weight.values())
    avg_temp = weighted_temp / total_weight
    avg_rainfall = weighted_rainfall / total_weight

    print(f"🌡️ Weighted Temperature: {avg_temp}°C | 🌧️ Weighted Rainfall: {avg_rainfall}mm")

    return avg_temp, avg_rainfall

# Function to adjust specific item categories based on weather
def adjust_special_stock(row, temperature, rainfall):
    if row['Category'] in ['beer', 'spirits'] or row['Item Name'] in ['Prosecco', 'Moet']:
        if temperature >= 16 and rainfall == 0:
            return math.ceil(row['Predicted Ordered Stock'] * 1.2)  # Increase by 20% for warm weather (weighted higher Fri-Sun)
        elif rainfall > 5:
            return math.ceil(row['Predicted Ordered Stock'] * 0.8)  # Decrease by 20% for wet weather (weighted higher Fri-Sun)
    return row['Predicted Ordered Stock']

# Load dataset
df = pd.read_csv("stock_orders_50_weeks.csv")

# Keep "Item Name" for output but REMOVE it from features
item_names = df["Item Name"]

# One-Hot Encode "Season"
df = pd.get_dummies(df, columns=["Season"])

# Define features (X) and target variable (y)
X = df[["Week", "Projected Covers", "Stock Left"] + list(df.filter(like="Season_").columns)]
y = df["Ordered Stock"]

# Normalize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build an MLP model
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(1)  # Output layer for stock prediction
])

model.compile(optimizer="adam", loss="mse")
model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=1)

# Predict next week's stock order for each item
last_week = df[df["Week"] == df["Week"].max()]  # Get latest week
next_week = last_week.copy()
next_week["Week"] += 1  # Predict for the next week

# Determine current season using the date
current_month = datetime.today().month
if current_month in [12, 1, 2]:
    next_week_season = 'Winter'
elif current_month in [3, 4, 5]:
    next_week_season = 'Spring'
elif current_month in [6, 7, 8]:
    next_week_season = 'Summer'
else:
    next_week_season = 'Fall'

# Add current season to MLP input
for season_col in df.filter(like="Season_").columns:
    next_week[season_col] = 0

next_week[f"Season_{next_week_season}"] = 1

# Predict stock orders
X_next_week = scaler.transform(next_week[["Week", "Projected Covers", "Stock Left"] + list(df.filter(like="Season_").columns)])
predicted_stock = model.predict(X_next_week)

next_week["Predicted Ordered Stock"] = [math.ceil(val[0]) for val in predicted_stock]

# Save predicted stock values to CSV
next_monday = datetime.today() + timedelta(days=(7 - datetime.today().weekday()))
filename = f"stockOrder_WC_{next_monday.strftime('%Y-%m-%d')}.csv"
next_week_with_season = pd.concat([next_week[["Item Name", "Predicted Ordered Stock"]], pd.DataFrame({"Item Name": ["Season"], "Predicted Ordered Stock": [next_week_season]})], ignore_index=True)
next_week_with_season.to_csv(filename, index=False)
print(f"🔮 Predictions saved to {filename}")
print(next_week[["Item Name", "Predicted Ordered Stock"]])
