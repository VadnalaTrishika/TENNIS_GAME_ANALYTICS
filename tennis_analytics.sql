CREATE DATABASE tennis_analytics;
USE tennis_analytics;

CREATE TABLE Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(255),
    type VARCHAR(50),
    gender VARCHAR(20),
    parent_id VARCHAR(50),
    category_id VARCHAR(50),
    FOREIGN KEY (category_id)
    REFERENCES Categories(category_id)
);

CREATE TABLE Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(255)
);

CREATE TABLE Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(255),
    city_name VARCHAR(100),
    country_name VARCHAR(100),
    timezone VARCHAR(100),
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id)
    REFERENCES Complexes(complex_id)
);

CREATE TABLE Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    competitor_name VARCHAR(255),
    country VARCHAR(100),
    country_code VARCHAR(10)
);

CREATE TABLE Competitor_Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    competitor_id VARCHAR(50),
    tour VARCHAR(50),
    gender VARCHAR(20),
    year INT,
    week INT,
    ranking_position INT,
    movement INT,
    points INT,
    competitions_played INT,
    FOREIGN KEY (competitor_id)
    REFERENCES Competitors(competitor_id)
);
SHOW TABLES;

SELECT COUNT(*) FROM Categories;
SELECT COUNT(*) FROM Competitions;
SELECT COUNT(*) FROM Complexes;
SELECT COUNT(*) FROM Competitors;
SELECT COUNT(*) FROM Competitor_Rankings;
SELECT COUNT(*) FROM Venues;

# Step 3: SQL Query Development 
# 1. Competitions Analysis:
# List all competitions with category names. 
SELECT
    c.competition_name,
    cat.category_name
FROM Competitions c
JOIN Categories cat
ON c.category_id = cat.category_id;

# Count the number of competitions in each category. 
SELECT
    cat.category_name,
    COUNT(*) AS competition_count
FROM Competitions c
JOIN Categories cat
ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY competition_count DESC;

# Find competitions of type ‘doubles’. 
SELECT * FROM Competitions
WHERE LOWER(type) = 'doubles';

# Get competitions in a specific category (e.g., ITF Men). 
SELECT c.competition_name,
    cat.category_name
FROM Competitions c
JOIN Categories cat
ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

# Identify parent competitions and their sub-competitions. 
SELECT
    p.competition_name AS parent_competition,
    c.competition_name AS sub_competition
FROM Competitions c
JOIN Competitions p
ON c.parent_id = p.competition_id;

# Analyze the distribution of competition types by category. 
SELECT
    cat.category_name,
    c.type,
    COUNT(*) AS total_competitions
FROM Competitions c
JOIN Categories cat
ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name;

# List all top-level competitions (no parent). 
SELECT *
FROM Competitions
WHERE parent_id IS NULL
   OR parent_id = '';
   
DESC Venues;
ALTER TABLE Venues
ADD COLUMN country_code VARCHAR(10);

# 2. Venue Analysis: 
# List all venues along with their associated complex names.
SELECT
    v.venue_name,
    c.complex_name
FROM Venues v
JOIN Complexes c
ON v.complex_id = c.complex_id;

# Count the number of venues in each complex. 
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM Complexes c
JOIN Venues v
ON c.complex_id = v.complex_id
GROUP BY c.complex_name
ORDER BY venue_count DESC;

# Get details of venues in a specific country. 
SELECT * FROM Venues
WHERE country_name = 'Spain';
SELECT * FROM Venues
WHERE country_name = 'Russia';

# Identify all venues with their timezones. 
SELECT
    venue_name,
    timezone
FROM Venues;

# Find complexes with more than one venue.
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM Complexes c
JOIN Venues v
ON c.complex_id = v.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

# List venues grouped by country. 
SELECT
    country_name,
    COUNT(*) AS total_venues
FROM Venues
GROUP BY country_name
ORDER BY total_venues DESC;

# Find all venues for a specific complex. 
SELECT complex_name FROM Complexes
LIMIT 10;
SELECT
    v.venue_name,
    c.complex_name
FROM Venues v
JOIN Complexes c
ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Melbourne Park';

# 3. Competitor Ranking Analysis: 
# Get all competitors with their rank and points. 
SELECT
    c.competitor_name,
    cr.ranking_position,
    cr.points
FROM Competitors c
JOIN Competitor_Rankings cr
ON c.competitor_id = cr.competitor_id
ORDER BY cr.ranking_position;

# Find competitors ranked in the top 5. 
SELECT
    c.competitor_name,
    cr.ranking_position,
    cr.points
FROM Competitors c
JOIN Competitor_Rankings cr
ON c.competitor_id = cr.competitor_id
WHERE cr.ranking_position <= 5
ORDER BY cr.ranking_position;

#  List competitors with no rank movement (stable rank). 
SELECT
    c.competitor_name,
    cr.ranking_position,
    cr.movement
FROM Competitors c
JOIN Competitor_Rankings cr
ON c.competitor_id = cr.competitor_id
WHERE cr.movement = 0;

# Get the total points of competitors from a specific country. 
SELECT
    c.country,
    SUM(cr.points) AS total_points
FROM Competitors c
JOIN Competitor_Rankings cr
ON c.competitor_id = cr.competitor_id
WHERE c.country = 'USA'
GROUP BY c.country;

# Count competitors per country. 
SELECT
    country,
    COUNT(*) AS competitor_count
FROM Competitors
GROUP BY country
ORDER BY competitor_count DESC;

# Find competitors with the highest points in the current week.
SELECT
    c.competitor_name,
    cr.points,
    cr.week,
    cr.year
FROM Competitors c
JOIN Competitor_Rankings cr
ON c.competitor_id = cr.competitor_id
WHERE cr.points = (
    SELECT MAX(points)
    FROM Competitor_Rankings
);

# For top 10
SELECT
    c.competitor_name,
    cr.points
FROM Competitors c
JOIN Competitor_Rankings cr
ON c.competitor_id = cr.competitor_id
ORDER BY cr.points DESC
LIMIT 10;