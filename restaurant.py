import sqlite3
import pandas as pd
import csv

def import_data(csv_file, db):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS restaurants")
    conn.commit()

    cq = '''CREATE TABLE restaurants (
	    id INTEGER, name TEXT, cuisine TEXT, allergies TEXT, 
        dietary restriction TEXT, nutritional value TEXT
        )'''  #creates the table restaurants
    cursor.execute(cq)

    #reads the csv file using pandas
    df= pd.read_csv(csv_file, header=None, delim_whitespace=False,
        names= ["id","name","cuisine","allergies", "dietary_restrictions", "nutritional_value"])
    data=[]
    
    for _, row in df.iterrows(): #iterates over the rows and appends them
        data.append((row["id"],row["name"], row["cuisine"], row["allergies"], row["dietary_restrictions"], row["nutritional_value"]))

    imq = '''INSERT INTO restaurants VALUES (?,?,?,?,?,?)'''

    cursor.executemany(imq, data)

    conn.commit()
    conn.close()


def prompt():

    cuisine_pref= input("Do you have any cuisine preferences?")
    allergies_pref= input("Do you have any allergies?")
    diet_pref= input("Do you have any dietary restrictions?")
    nutrition_pref= input("Do you have any nutritional goals?")
    return cuisine_pref, allergies_pref, diet_pref, nutrition_pref

def recommend(csv_file,cuisine_pref, allergies_pref, diet_pref, nutrition_pref):

    df= pd.read_csv(csv_file, header=None, delim_whitespace=False,
        names= ["id","name","cuisine","allergies", "dietary_restrictions", "nutritional_value"])

    recommendation= df[(df["cuisine"].str.contains(cuisine_pref,na=False)) &
        (df["allergies"].str.contains(allergies_pref,na=False)) & 
        (df["dietary_restrictions"].str.contains(diet_pref,na=False))&
        (df["nutritional_value"].str.contains(nutrition_pref,na=False))]
    
    return recommendation

if __name__== "__main__":

    import_data("restaurants.csv", "restaurants.db")

    cuisine_pref, allergies_pref, diet_pref, nutrition_pref= prompt()

    rec= recommend("restaurants.csv", cuisine_pref, allergies_pref, diet_pref, nutrition_pref)


    print(f"Your recommended restaurants are {rec}")