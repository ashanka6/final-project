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
    df= pd.read_csv(csv_file,  delim_whitespace=False, usecols=[0, 3], names= ["name","type"])
    df = df.dropna(subset=["type"])

    #df["type_attribute"] = df["type"].str.split(",")

    data = []

    for _, row in df.iterrows():
        name = row["name"].strip()
        type = [type_attr.strip().lower() for type_attr in row["type"].split(',') if type_attr.strip()]
        for type_attr in type:
            data.append((name, type_attr))


    imq = '''INSERT INTO restaurants (name,type) VALUES (?,?)'''

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

    preferences = []

    if cuisine_pref:
        preferences.append(cuisine_pref.lower())
    if gluten_pref == "yes":
        preferences.append("gluten free options")
    if diet_pref:
        preferences.append(diet_pref.lower())
    if dining_pref:
        preferences.append(dining_pref.lower())
    recommendations = cursor.fetchall()

    if not preferences:
        cursor.execute("SELECT DISTINCT name FROM restaurants")
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results

    placeholders = ",".join("?" for _ in preferences)

    query = f"""
        SELECT name
        FROM restaurants
        WHERE type IN ({placeholders})
        GROUP BY name
        HAVING COUNT(DISTINCT type) = ?
    """
    cursor.execute(query, (*preferences, len(preferences)))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

if __name__== "__main__":

    import_data("Restaurants.csv", "restaurants.db")

    cuisine_pref, gluten_pref, diet_pref, dining_pref= prompt()

    rec= recommend("restaurants.db", cuisine_pref, gluten_pref, diet_pref, dining_pref)

    print(f"Your recommended restaurants are {rec}")
