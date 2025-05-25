import sqlite3
import random

# Connect to SQLite
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        table_count INTEGER,
        table_size INTEGER,
        rating REAL,
        avg_amount_per_person REAL
    )
''')

# Shared sample data for variety
locations = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune"]
ratings = [4.0, 4.2, 4.5, 4.7, 4.8]
avg_amounts = [300, 350, 400, 450, 500, 600, 700, 800]
table_sizes = [2, 4, 6]
table_counts = [10, 15, 20, 25, 30]

# Restaurant name base for uniqueness
base_names = [
    "Spice Villa", "Curry Kingdom", "Tandoori Nights", "Pasta Palace", "Sushi World",
    "Burger Hub", "Taco Town", "Dimsum Den", "Pizza Planet", "Biryani Bistro",
    "Grill House", "Masala Magic", "The Kebab Room", "Food Fiesta", "Ocean Delights",
    "Taj", "Royal Feast", "Gastronomy Garden", "Savory Street", "Taste Temple", "Flavor Fusion",
    "Culinary Canvas", "Epicurean Escape", "Gourmet Galaxy", "Delightful Dishes", "Heavenly Bites",
    "Savory Symphony", "Taste Odyssey", "Gastronomic Getaway", "Epicurean Euphoria", "Flavor Haven", 
    "Culinary Cove", "Gastronomic Gala", "Epicurean Eden", "Tasteful Treasures", "Savory Sanctuary",
    "Flavor Fiesta", "Culinary Carnival", "Gastronomic Garden", "Epicurean Experience", "Tasteful Temptations",
]

# Generate 50 entries
restaurant_data = []
for i in range(35):
    name = base_names[i]
    location = random.choice(locations)
    table_count = random.choice(table_counts)
    table_size = random.choice(table_sizes)
    rating = random.choice(ratings)
    avg_amount = random.choice(avg_amounts)

    restaurant_data.append((name, location, table_count, table_size, rating, avg_amount))

# Insert into DB
cursor.executemany('''
    INSERT INTO restaurants (name, location, table_count, table_size, rating, avg_amount_per_person)
    VALUES (?, ?, ?, ?, ?, ?)
''', restaurant_data)

conn.commit()
conn.close()

print("35 dummy restaurant records inserted successfully.")
