"""A file to test the database.py file.

Driver: 
Navigator: 
Assignment: Final Project
Date: 5_10_25

Challenges Encountered: making the unit tests
""" 
import unittest 
import sqlite3 

class TestRestaurantDatabase(unittest.TestCase): 
    def setUp(self): 
        # Connect to the SQLite database in memory for testing 
        self.conn = sqlite3.connect(':memory:') 
        self.db = RestaurantDatabase("restaurant.db")
        self.create_tables() 
        # Create the tables for testing 
    def create_tables(self): 
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

        self.conn.commit() 

    def test_insert_meal(self): 
        pass 

    def tearDown(self): 
        # Close the database connection after each test 
        self.conn.close() 

if __name__ == '__main__': 
    unittest.main() 