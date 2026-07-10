# Game Analytics: Unlocking Tennis Data with SportRadar API

## Project Objective

The objective of this project is to collect tennis data from the SportRadar API, store it in a MySQL database, perform SQL-based analysis, and develop an interactive Streamlit dashboard to analyze competitions, venues, and competitor rankings.

## Setup Instructions

### Step 1: Install Required Libraries

pip install pandas requests streamlit mysql-connector-python plotly

### Step 2: Create MySQL Database

CREATE DATABASE tennis_analytics;
USE tennis_analytics;

### Step 3: Run Data Extraction Scripts

python api_competitions.py

python api_complexes.py

python api_rankings.py

python venues.py

### Step 4: Load Data into MySQL

Run the SQL script and import the extracted CSV files into the corresponding MySQL tables.

### Step 5: Run the Streamlit Application

Before running the project, replace YOUR_API_KEY with a valid SportRadar API key.

streamlit run app.py

## Demo Walkthrough

### Dashboard
Displays total competitors, countries represented, and highest ranking points.

### Competitor Explorer
Allows users to search competitors and apply filters.

### Competitor Details
Displays player ranking, points, movement, and competitions played.

### Country Analysis
Provides country-wise competitor statistics and average points.

### Leaderboards
Displays top-ranked competitors and highest-scoring players.

## Conclusion

This project integrates SportRadar API data extraction, MySQL database management, SQL analytics, and Streamlit visualization to provide meaningful insights into tennis competitions and player rankings.