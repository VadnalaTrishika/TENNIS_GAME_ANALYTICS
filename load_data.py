import pandas as pd
import mysql.connector

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="tennis_analytics"
)

cursor = conn.cursor()

# -----------------------
# Load Competitions CSV
# -----------------------
competitions = pd.read_csv("competitions.csv")

# Insert Categories
categories = competitions[['category_id', 'category_name']].drop_duplicates()

for _, row in categories.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Categories(category_id, category_name)
        VALUES (%s, %s)
    """, (
        row['category_id'],
        row['category_name']
    ))

# Insert Competitions
for _, row in competitions.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Competitions
        (competition_id, competition_name, type, gender, parent_id, category_id)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        row['competition_id'],
        row['competition_name'],
        row['type'],
        row['gender'],
        row['parent_id'],
        row['category_id']
    ))

# -----------------------
# Load Complexes CSV
# -----------------------
complexes = pd.read_csv("complexes.csv")

for _, row in complexes.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Complexes
        (complex_id, complex_name)
        VALUES (%s,%s)
    """, (
        row['complex_id'],
        row['complex_name']
    ))

# -----------------------
# Load Rankings CSV
# -----------------------
rankings = pd.read_csv("rankings.csv")

# Insert Competitors
competitors = rankings[
    ['competitor_id', 'competitor_name', 'country', 'country_code']
].drop_duplicates()

for _, row in competitors.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Competitors
        (competitor_id, competitor_name, country, country_code)
        VALUES (%s,%s,%s,%s)
    """, (
        row['competitor_id'],
        row['competitor_name'],
        row['country'],
        row['country_code']
    ))

# Insert Rankings
for _, row in rankings.iterrows():
    cursor.execute("""
        INSERT INTO Competitor_Rankings
        (competitor_id, tour, gender, year, week,
         ranking_position, movement, points, competitions_played)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row['competitor_id'],
        row['tour'],
        row['gender'],
        row['year'],
        row['week'],
        row['rank'],
        row['movement'],
        row['points'],
        row['competitions_played']
    ))

conn.commit()

print("Data loaded successfully!")

cursor.close()
conn.close()