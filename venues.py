# Import required libraries
import requests
import pandas as pd

# SportRadar API Key
API_KEY = "YOUR_API_KEY"

# Venues endpoint
url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"

# API request headers
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

# Fetch data from API
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    print("Status Code:", response.status_code)

    data = response.json()

except requests.exceptions.RequestException as e:
    print("API Request Failed:", e)
    exit()

# Store venue records
venues = []

for comp in data["complexes"]:

    complex_id = comp.get("id")

    for venue in comp.get("venues", []):

        venues.append({
            "venue_id": venue.get("id"),
            "venue_name": venue.get("name"),
            "city_name": venue.get("city_name"),
            "country_name": venue.get("country_name"),
            "country_code": venue.get("country_code"),
            "timezone": venue.get("timezone"),
            "complex_id": complex_id
        })

# Convert JSON to DataFrame
df = pd.DataFrame(venues)

print(df.head())

# Save data to CSV
df.to_csv("venues.csv", index=False)

print("Venues data saved successfully!")