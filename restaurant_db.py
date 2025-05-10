import sqlite3
import pandas as pd

# Connect to SQLite database (creates the DB if not exists)
conn = sqlite3.connect('restaurants.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS restaurants')
cursor.execute('DROP TABLE IF EXISTS cuisines')
cursor.execute('DROP TABLE IF EXISTS allergies')
cursor.execute('DROP TABLE IF EXISTS nutritional_goals')
cursor.execute('DROP TABLE IF EXISTS meals')

# Create tables
cursor.execute('''CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    rating REAL,
    price_range TEXT
)''')

cursor.execute('''CREATE TABLE cuisines (
    cuisine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine_name TEXT
)''')

cursor.execute('''CREATE TABLE allergies (
    allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    allergy_name TEXT
)''')

cursor.execute('''CREATE TABLE nutritional_goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_name TEXT
)''')

cursor.execute('''CREATE TABLE meals (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    meal_name TEXT,
    calories INTEGER,
    protein INTEGER,
    fats INTEGER,
    carbs INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
)''')

# Junction tables for many-to-many relationships
cursor.execute('''CREATE TABLE restaurant_cuisines (
    restaurant_id INTEGER,
    cuisine_id INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (cuisine_id) REFERENCES cuisines(cuisine_id)
)''')

cursor.execute('''CREATE TABLE restaurant_allergies (
    restaurant_id INTEGER,
    allergy_id INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (allergy_id) REFERENCES allergies(allergy_id)
)''')

cursor.execute('''CREATE TABLE restaurant_nutritional_goals (
    restaurant_id INTEGER,
    goal_id INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (goal_id) REFERENCES nutritional_goals(goal_id)
)''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully.")
