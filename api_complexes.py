# Import required libraries
import requests
import pandas as pd

# SportRadar API Key
API_KEY = "YOUR_API_KEY"

# Complexes endpoint
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

# Store complex records
complexes = []

for comp in data["complexes"]:

    complexes.append({
        "complex_id": comp.get("id"),
        "complex_name": comp.get("name")
    })

# Convert JSON to DataFrame
df = pd.DataFrame(complexes)

print(df.head())

# Save data to CSV
df.to_csv("complexes.csv", index=False)

print("Complexes data saved successfully!")