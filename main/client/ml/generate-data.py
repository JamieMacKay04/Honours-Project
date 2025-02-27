import pandas as pd
import random

# Define stock items (from your images)
stock_items = [
    ("Apple Juice", "Soft Drinks"), ("Bacardi Blanco", "Spirits"), ("Bira Moretti", "Beer"),
    ("Bombay Gin", "Spirits"), ("Captain Morgan Spiced Rum", "Spirits"), ("Chardonnay", "Wine"),
    ("Coca Cola", "Soft Drinks"), ("Coke Zero", "Soft Drinks"), ("Cointreau", "Spirits"),
    ("Corona", "Beer"), ("Cranberry Juice", "Soft Drinks"), ("Dalmore 12", "Spirits"),
    ("Diet Coke", "Soft Drinks"), ("Disaronno", "Spirits"), ("Havana Club 3", "Spirits"),
    ("Havana Club 7", "Spirits"), ("High Commissioner", "Spirits"), ("Irn Bru", "Soft Drinks"),
    ("J20", "Soft Drinks"), ("Jack Daniels", "Spirits"), ("Kahlua", "Spirits"),
    ("Lemonade", "Soft Drinks"), ("Light Tonic", "Soft Drinks"), ("Limoncello", "Spirits"),
    ("Macallan 12", "Spirits"), ("Malbec", "Wine"), ("Martini Rosso", "Spirits"),
    ("Merlot", "Wine"), ("Moet", "Wine"), ("Orange Juice", "Soft Drinks"),
    ("Passoa", "Spirits"), ("Peroni", "Beer"), ("Pineapple Juice", "Soft Drinks"),
    ("Pink Gin", "Spirits"), ("Pinot Grigio", "Wine"), ("Prosecco", "Wine"),
    ("Rijoca", "Wine"), ("Sauvignon Blanc", "Wine"), ("St Germain", "Spirits"),
    ("Tanqueray 10", "Spirits"), ("Tonic Water", "Soft Drinks")
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
