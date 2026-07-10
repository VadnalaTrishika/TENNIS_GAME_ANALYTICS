# Import required libraries
import requests
import pandas as pd

# SportRadar API Key
API_KEY = "YOUR_API_KEY"

# Rankings endpoint
url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

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

# Store ranking records
rankings = []

for ranking_group in data["rankings"]:

    for player in ranking_group["competitor_rankings"]:

        rankings.append({
            "tour": ranking_group.get("name"),
            "gender": ranking_group.get("gender"),
            "year": ranking_group.get("year"),
            "week": ranking_group.get("week"),
            "rank": player.get("rank"),
            "movement": player.get("movement"),
            "points": player.get("points"),
            "competitions_played": player.get("competitions_played"),
            "competitor_id": player.get("competitor", {}).get("id"),
            "competitor_name": player.get("competitor", {}).get("name"),
            "country": player.get("competitor", {}).get("country"),
            "country_code": player.get("competitor", {}).get("country_code")
        })

# Convert JSON to DataFrame
df = pd.DataFrame(rankings)

print(df.head())

# Save data to CSV
df.to_csv("rankings.csv", index=False)

print("Rankings data saved successfully!")