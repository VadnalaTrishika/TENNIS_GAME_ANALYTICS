import pandas as pd
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="tennis_analytics"
)

cursor = conn.cursor()

venues = pd.read_csv("venues.csv")

for _, row in venues.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Venues
        (venue_id, venue_name, city_name,
         country_name, country_code,
         timezone, complex_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        row['venue_id'],
        row['venue_name'],
        row['city_name'],
        row['country_name'],
        row['country_code'],
        row['timezone'],
        row['complex_id']
    ))

conn.commit()

print("Venues loaded successfully!")

cursor.close()
conn.close()