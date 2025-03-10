import pandas as pd
import random

# Define stock items (from your images)
stock_items = [
    ("Apple Juice", "soft drinks"), ("Bacardi Blanco", "spirits"), ("Bira Moretti", "beer"),
    ("Bombay Gin", "spirits"), ("Captain Morgan Spiced Rum", "spirits"), ("Chardonnay", "wine"),
    ("Coca Cola", "soft drinks"), ("Coke Zero", "soft drinks"), ("Cointreau", "spirits"),
    ("Corona", "beer"), ("Cranberry Juice", "soft drinks"), ("Dalmore 12", "spirits"),
    ("Diet Coke", "soft drinks"), ("Disaronno", "spirits"), ("Havana Club 3", "spirits"),
    ("Havana Club 7", "spirits"), ("High Commissioner", "spirits"), ("Irn Bru", "soft drinks"),
    ("J20", "soft drinks"), ("Jack Daniels", "spirits"), ("Kahlua", "spirits"),
    ("Lemonade", "soft drinks"), ("Light Tonic", "soft drinks"), ("Limoncello", "spirits"),
    ("Macallan 12", "spirits"), ("Malbec", "wine"), ("Martini Rosso", "spirits"),
    ("Merlot", "wine"), ("Moet", "wine"), ("Orange Juice", "soft drinks"),
    ("Passoa", "spirits"), ("Peroni", "beer"), ("Pineapple Juice", "soft drinks"),
    ("Pink Gin", "spirits"), ("Pinot Grigio", "wine"), ("Prosecco", "wine"),
    ("Rijoca", "wine"), ("Sauvignon Blanc", "wine"), ("St Germain", "spirits"),
    ("Tanqueray 10", "spirits"), ("Tonic Water", "soft drinks")
]

# Define seasons
seasons = ["Winter", "Spring", "Summer", "Fall"]

# Generate 50 weeks of data
data = []
for week in range(1, 51):  # 50 weeks
    season = seasons[(week // 13) % 4]  # Rotate seasons every 13 weeks
    for item, category in stock_items:
        ordered_stock = random.randint(5, 50)  # Random realistic stock order
        projected_covers = random.randint(100, 500)  # Random customer estimates
        stock_left = max(0, ordered_stock - random.randint(0, 20))  # Simulating leftover stock

        data.append([week, item, category, ordered_stock, projected_covers, stock_left, season])

# Create DataFrame
df = pd.DataFrame(data, columns=["Week", "Item Name", "Category", "Ordered Stock", "Projected Covers", "Stock Left", "Season"])

# Save to CSV
df.to_csv("stock_orders_50_weeks.csv", index=False)

print("CSV file generated successfully!")
