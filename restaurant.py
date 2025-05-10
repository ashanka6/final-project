import sqlite3
import pandas as pd
import csv


def import_data(csv_file, db):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS restaurants")
    conn.commit()

    cq = '''CREATE TABLE restaurants (
	    name TEXT, type TEXT
        )'''  #creates the table restaurants
    cursor.execute(cq)

    #reads the csv file using pandas
    df= pd.read_csv(csv_file,  delim_whitespace=False, usecols=[0, 3],
        names= ["name","type"])
    
    df = df.dropna(subset=["type"])
    df["type_attribute"] = df["type"].str.split(",")


    data = []

    for _, row in df.iterrows():
        for attribute in row['type_attribute']:
            data.append((row["name"], attribute.strip()))


    imq = '''INSERT INTO restaurants VALUES (?,?)'''

    cursor.executemany(imq, data)

    conn.commit()
    conn.close()


def prompt():

    cuisine_pref= input("Do you have any cuisine preferences?(America, Italian, etc) Type 'no' if not ").lower()
    gluten_pref= input("Are you gluten free? Type 'no' if not ").lower()
    diet_pref= input("Do you have any dietary restrictions?(Vegan or Vegetarian) Type 'no' if not ").lower()
    dining_pref= input("Would you prefer a specific dining experience? (Bar, Wine Bar, Cafe) Type 'no' if not ").lower()

    if cuisine_pref == "no":
        cuisine_pref=None
    if gluten_pref == "no":
        gluten_pref=None
    if diet_pref =="no":
        diet_pref=None
    if dining_pref=="no":
        dining_pref= None

    return cuisine_pref, gluten_pref, diet_pref,dining_pref

def recommend(db,cuisine_pref, gluten_pref, diet_pref, dining_pref):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    prefs=[]

    query = '''SELECT DISTINCT name
    FROM restaurants
    where 1=1'''

    if cuisine_pref:
        query += " AND type LIKE ?"
        prefs.append(f'%{cuisine_pref}%')

    if gluten_pref:
        if gluten_pref == 'yes':
            query += " AND type LIKE ?"
            prefs.append('%Gluten Free Options%')

    if diet_pref:
        query += " AND type LIKE ?"
        prefs.append(f'%{diet_pref}%')

    if dining_pref:
        query += " AND type LIKE ?"
        prefs.append(f'%{dining_pref}%')

    if prefs:
        cursor.execute(query, prefs)
    else:
        cursor.execute(query)

    recommendations = cursor.fetchall()

    conn.close()

    return recommendations

if __name__== "__main__":

    import_data("Restaurants.csv", "restaurants.db")

    cuisine_pref, gluten_pref, diet_pref, dining_pref= prompt()

    rec= recommend("restaurants.db", cuisine_pref, gluten_pref, diet_pref, dining_pref)

    print(f"Your recommended restaurants are {rec}")
