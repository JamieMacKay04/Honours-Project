import csv
from pymongo import MongoClient

# MongoDB Connection Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "mydatabase"
COLLECTION_NAME = "stockitems"

# Function to connect to MongoDB
def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db[COLLECTION_NAME]

# Function to read CSV data, modify field names, and set appropriate units
def read_csv_data(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        data = []
        for row in csv_reader:
            row.pop('Projected Covers', None)  # Remove 'Projected Covers' if present
            
            # Handle 'Predicted Ordered Stock' ➔ 'quantity' (converted to int)
            if 'Predicted Ordered Stock' in row:
                try:
                    row['quantity'] = int(float(row.pop('Predicted Ordered Stock')))
                except ValueError:
                    print(f"⚠️ Invalid quantity for {row['Item Name']}. Skipping entry.")
                    continue  # Skip invalid entries

            # Unit & Quantity Handling
            if row['Category'].strip().lower() == 'spirits':
                row['unit'] = 'mL'
                row['quantity'] *= 1000  # Convert to mL for new entries only
                row['converted'] = True  # Flag to mark converted items
            else:
                row['unit'] = 'bottle'  # Non-spirits remain in bottles
            
            data.append(row)
        return data

# Function to insert or aggregate data in MongoDB
def insert_data(collection, data):
    for item in data:
        query = {"Item Name": item["Item Name"]}

        # Check if item already exists
        existing_item = collection.find_one(query)

        if existing_item:
            existing_quantity = int(existing_item.get("quantity", 0))
            
            # If item is a spirit, add mL values directly (skip multiplying by 1000 again)
            if item['unit'] == 'mL':
                new_quantity = existing_quantity + item['quantity']  # No extra multiplication
            else:
                new_quantity = existing_quantity + item['quantity']

            update = {"$set": {"quantity": new_quantity, "unit": item["unit"]}}
            collection.update_one(query, update)
            print(f"🔄 Updated {item['Item Name']} ➔ New Quantity: {new_quantity} {item['unit']} ✅")
        else:
            # Insert as a new entry
            collection.insert_one(item)
            print(f"✅ Inserted: {item['Item Name']} ➔ Quantity: {item['quantity']} {item['unit']}")

# Main Execution Flow
if __name__ == "__main__":
    csv_file_path = "newOrder.csv"

    # Step 1: Read CSV data
    try:
        data = read_csv_data(csv_file_path)
        if not data:
            print("❌ No data found in CSV file.")
            exit()
    except FileNotFoundError:
        print(f"❌ Error: CSV file '{csv_file_path}' not found.")
        exit()

    # Step 2: Connect to MongoDB and Insert/Aggregate Data
    try:
        collection = connect_to_mongo()
        insert_data(collection, data)
        print("🚀 Database update completed successfully!")
    except Exception as e:
        print(f"❌ Database error: {e}")
