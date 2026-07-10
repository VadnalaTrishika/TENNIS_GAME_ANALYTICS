# Import required libraries
import requests
import pandas as pd

# SportRadar API key
API_KEY = "YOUR_API_KEY"

# Competitions endpoint
url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"

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

# Store competition records
competitions = []

for comp in data["competitions"]:

    competitions.append({
        "competition_id": comp.get("id"),
        "competition_name": comp.get("name"),
        "type": comp.get("type"),
        "gender": comp.get("gender"),
        "parent_id": comp.get("parent_id"),
        "category_id": comp.get("category", {}).get("id"),
        "category_name": comp.get("category", {}).get("name")
    })

# Convert JSON data to DataFrame
df = pd.DataFrame(competitions)

print(df.head())

# Save data as CSV
df.to_csv("competitions.csv", index=False)

print("Competitions data saved successfully!")