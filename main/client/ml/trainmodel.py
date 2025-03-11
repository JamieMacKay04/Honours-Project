import pandas as pd
import numpy as np
import math  # ✅ Import math for rounding up
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# ✅ Load dataset
df = pd.read_csv("stock_orders_50_weeks.csv")

# ✅ Keep "Item Name" for output but REMOVE it from features
item_names = df["Item Name"]

# ✅ One-Hot Encode "Season"
df = pd.get_dummies(df, columns=["Season"])  

# ✅ Define features (X) and target variable (y)
X = df[["Week", "Projected Covers", "Stock Left"] + list(df.filter(like="Season_").columns)]
y = df["Ordered Stock"]

# ✅ Normalize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ✅ Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ✅ Build an MLP model
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(1)  # Output layer for stock prediction
])

model.compile(optimizer="adam", loss="mse")
model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=1)

# ✅ Predict next week's stock order for each item
last_week = df[df["Week"] == df["Week"].max()]  # Get latest week
next_week = last_week.copy()
next_week["Week"] += 1  # Predict for the next week

# Remove "Item Name" before prediction
X_next_week = scaler.transform(next_week[["Week", "Projected Covers", "Stock Left"] + list(df.filter(like="Season_").columns)])
predicted_stock = model.predict(X_next_week)

# ✅ Round up predicted values
next_week["Predicted Ordered Stock"] = [math.ceil(val[0]) for val in predicted_stock]

# ✅ Print predictions with item names
print("\n🔮 Predicted Stock Order for Next Week:")
print(next_week[["Item Name", "Predicted Ordered Stock"]])