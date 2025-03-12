import os
import pandas as pd
import math
from datetime import datetime

# Ensure correct path to the stockOrders.csv file
stock_orders_path = os.path.join(os.getcwd(), 'client/ml/stockOrders.csv')

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Check if stockOrders.csv exists
if not os.path.exists(stock_orders_path):
    print(f"Error: {stock_orders_path} not found.")
else:
    # Load dataset
    df = pd.read_csv(stock_orders_path)

    # One-Hot Encode 'Item Name'
    df = pd.get_dummies(df, columns=["Item Name"], prefix="Item")

    # Define features (X) and target variable (y)
    X = df[[ "Week", "Projected Covers", "Stock Left"
    ] + list(df.filter(like="Season_").columns) + list(df.filter(like="Item_").columns)]
    y = df["Ordered Stock"]

    # Normalize numerical features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/Test Split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Build Improved MLP Model
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    model = Sequential([
        Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
        Dense(64, activation="relu"),
        Dense(32, activation="relu"),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")
    model.fit(X_train, y_train, epochs=100, batch_size=8, verbose=1)

    # Predict next week's stock order for each item
    last_week = df[df["Week"] == df["Week"].max()]
    next_week = last_week[[
        "Week", "Category", "Ordered Stock", "Projected Covers", "Stock Left"
    ] + list(df.filter(like="Item_").columns)].copy()

    # Add season data for next week
    current_month = datetime.today().month
    if current_month in [12, 1, 2]:
        next_week_season = 'Winter'
    elif current_month in [3, 4, 5]:
        next_week_season = 'Spring'
    elif current_month in [6, 7, 8]:
        next_week_season = 'Summer'
    else:
        next_week_season = 'Fall'

    next_week["Season"] = next_week_season
    next_week["Week"] += 1

    # Ensure One-Hot Encoded 'Item Name' data is filled properly
    for col in X.columns:
        if col not in next_week.columns:
            next_week[col] = 0

    # Predict Projected Covers for next week
    temp, rain = get_weather_forecast()
    last_week_covers = last_week['Projected Covers'].mean()
    if temp >= 16 and rain == 0:
        next_week['Projected Covers'] = int(last_week_covers * 1.2)
    elif rain > 5:
        next_week['Projected Covers'] = int(last_week_covers * 0.8)
    else:
        next_week['Projected Covers'] = int(last_week_covers)

    # Scale features for prediction
    X_next_week = scaler.transform(next_week[X.columns])
    predicted_stock = model.predict(X_next_week)

    # Add predicted stock values to 'next_week'
    next_week["Predicted Ordered Stock"] = [math.ceil(val[0]) for val in predicted_stock]

    # ✅ Restore 'Item Name' for CSV and logs
    item_columns = [col for col in next_week.columns if col.startswith("Item_")]
    next_week['Item Name'] = next_week[item_columns].idxmax(axis=1).str.replace('Item_', '')

    # 🔹 Save to `newOrder.csv` (Only Item Name, Category, Predicted Ordered Stock)
    new_order_data = next_week[["Item Name", "Category", "Predicted Ordered Stock"]].copy()
    new_order_data.to_csv("newOrder.csv", index=False)
    print("✅ Predictions successfully saved to 'newOrder.csv'")

    # 🔹 Continue updating 'stockOrders.csv'
    next_week["Week"] = df["Week"].max() + 1  # Last week + 1

    # Load the existing stockOrders.csv (or create it if missing)
    try:
        stock_order_df = pd.read_csv(stock_orders_path)
    except FileNotFoundError:
        stock_order_df = pd.DataFrame(columns=[
            "Week", "Item Name", "Category", "Ordered Stock",
            "Projected Covers", "Stock Left", "Season", "Predicted Ordered Stock"
        ])

    # Append the new predictions to the existing data
    stock_order_df = pd.concat([stock_order_df, next_week], ignore_index=True)

    # Save the updated file
    stock_order_df.to_csv(stock_orders_path, index=False)

    print("✅ Predictions successfully added to 'stockOrders.csv'")
