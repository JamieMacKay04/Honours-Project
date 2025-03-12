import pandas as pd
import random

# Define stock items
stock_items = [
    ("Apple Juice", "soft drinks"), ("Aperol", "spirits"), ("Bacardi Blanco", "spirits"),
    ("Bira Moretti", "beer"), ("Bombay Gin", "spirits"), ("Captain Morgan Spiced Rum", "spirits"),
    ("Chardonnay", "wine"), ("Coca Cola", "soft drinks"), ("Coke Zero", "soft drinks"),
    ("Cointreau", "spirits"), ("Corona", "beer"), ("Cranberry Juice", "soft drinks"),
    ("Dalmore 12", "spirits"), ("Diet Coke", "soft drinks"), ("Disaronno", "spirits"),
    ("Finlandia Vodka", "spirits"), ("Havana Club 3", "spirits"), ("Havana Club 7", "spirits"),
    ("High Commissioner", "spirits"), ("Irn Bru", "soft drinks"), ("J20", "soft drinks"),
    ("Jack Daniels", "spirits"), ("Kahlua", "spirits"), ("Lemonade", "soft drinks"),
    ("Light Tonic", "soft drinks"), ("Limoncello", "spirits"), ("Macallan 12", "spirits"),
    ("Malbec", "wine"), ("Martini Rosso", "spirits"), ("Merlot", "wine"), ("Moet", "wine"),
    ("Orange Juice", "soft drinks"), ("Passoa", "spirits"), ("Peroni", "beer"),
    ("Pineapple Juice", "soft drinks"), ("Pink Gin", "spirits"), ("Pinot Grigio", "wine"),
    ("Prosecco", "wine"), ("Rijoca", "wine"), ("Sauvignon Blanc", "wine"),
    ("St Germain", "spirits"), ("Tanqueray 10", "spirits"), ("Tonic Water", "soft drinks")
]

# Define house pours
house_pours = ["Finlandia Vodka", "Captain Morgan Spiced Rum", "Bombay Gin"]

# Define special soft drinks
special_softdrinks = ["Coca Cola", "Tonic Water", "Diet Coke", "Coke Zero", "Lemonade"]

# Define seasons
seasons = ["Winter", "Spring", "Summer", "Fall"]

# Generate 50 weeks of data
data = []
for week in range(1, 51):
    season = seasons[(week // 13) % 4]
    base_projected_covers = random.randint(50, 250)

    # Seasonal adjustment for Projected Covers
    if season == "Summer":
        projected_covers = int(base_projected_covers * 1.5)
    elif season == "Winter":
        projected_covers = int(base_projected_covers * 0.6)
    else:
        projected_covers = base_projected_covers

    for item, category in stock_items:
        # Custom House Pours & Spirits Logic
        if item in house_pours:
            base_stock = random.randint(2, 6)  # House pours ➔ 2 to 6 bottles
        elif category == "spirits":
            base_stock = random.randint(0, 2)  # Other spirits ➔ 0 to 2 bottles
        elif item == "Aperol" and season == "Summer":
            base_stock = random.randint(0, 4)
        elif category == "wine":
            base_stock = random.randint(2, 10)
        elif category == "soft drinks" and item not in special_softdrinks:
            base_stock = random.randint(5, 12)
        else:
            base_stock = random.randint(7, 35)

        # Seasonal adjustment for stock orders with hard limits for spirits
        if season == "Summer":
            ordered_stock = int(base_stock * 1.5)
        elif season == "Winter":
            ordered_stock = int(base_stock * 0.6)
        else:
            ordered_stock = base_stock

        # ✅ Add hard cap to enforce maximum values for spirits
        if category == "spirits":
            if item in house_pours:
                ordered_stock = max(2, min(6, ordered_stock))  # House pours range: 2-6
            else:
                ordered_stock = max(0, min(2, ordered_stock))  # Other spirits range: 0-2

        stock_left = max(0, ordered_stock - random.randint(0, 20))

        data.append([week, item, category, ordered_stock, projected_covers, stock_left, season])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "Week", "Item Name", "Category", "Ordered Stock",
    "Projected Covers", "Stock Left", "Season"
])

# Save to CSV
df.to_csv("stockOrders.csv", index=False)

print("✅ CSV file generated successfully!")
