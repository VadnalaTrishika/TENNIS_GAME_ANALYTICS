"""
Game Analytics: Unlocking Tennis Data with SportRadar API

This application connects to a MySQL database and provides
interactive tennis analytics through Streamlit dashboards.
Features include competitor search, country analysis,
leaderboards, and ranking insights.
"""

import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(
    page_title="Tennis Analytics Hub",
    page_icon="🎾",
    layout="wide"
)

# Database Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="tennis_analytics"
    )

    cursor = conn.cursor()

except mysql.connector.Error as e:
    st.error(f"Database Connection Error: {e}")
    st.stop()

# Title
st.title("🎾 Tennis Analytics Hub")
st.subheader("Player Rankings & Performance Dashboard")

# Fetch KPI metrics for dashboard
cursor.execute("SELECT COUNT(*) FROM Competitors")
total_competitors = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT country) FROM Competitors")
total_countries = cursor.fetchone()[0]

cursor.execute("SELECT MAX(points) FROM Competitor_Rankings")
highest_points = cursor.fetchone()[0]


# Sidebar navigation
st.sidebar.title("🎾 Navigation")

# Navigation menu
page = st.sidebar.radio(
    "Go To",
    [
        "🏠 Dashboard",
        "🔍 Competitor Explorer",
        "👤 Competitor Details",
        "🌍 Country Analysis",
        "🏆 Leaderboards"
    ]
)
# Dashboard Page
if page == "🏠 Dashboard":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👤 Total Competitors", total_competitors)

    with col2:
        st.metric("🌍 Countries", total_countries)

    with col3:
        st.metric("🏆 Highest Points", highest_points)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        country_df = pd.read_sql("""
        SELECT country,
               COUNT(*) AS total_players
        FROM Competitors
        GROUP BY country
        ORDER BY total_players DESC
        LIMIT 10
        """, conn)

        st.subheader("🌍 Top 10 Countries by Competitors")
        st.bar_chart(country_df.set_index("country"))

    with col2:

        ranking_df = pd.read_sql("""
        SELECT ranking_position, points
        FROM Competitor_Rankings
        ORDER BY ranking_position
        LIMIT 50
        """, conn)

        st.subheader("📈 Ranking vs Points")
        st.line_chart(
            ranking_df.set_index("ranking_position")
        )

# Competitor Explorer Page
elif page == "🔍 Competitor Explorer":

    st.header("🔍 Competitor Search & Filter")

    search_name = st.text_input("Search Competitor")

    countries = pd.read_sql(
        "SELECT DISTINCT country FROM Competitors ORDER BY country",
        conn
    )

    selected_country = st.selectbox(
        "Select Country",
        ["All"] + countries["country"].tolist()
    )

    rank_range = st.slider(
        "Rank Range",
        1,
        1000,
        (1,100)
    )

    min_points = st.slider(
        "Minimum Points",
        0,
        11000,
        0
    )

    query = """
    SELECT
        c.competitor_name,
        c.country,
        cr.ranking_position,
        cr.points
    FROM Competitors c
    JOIN Competitor_Rankings cr
    ON c.competitor_id = cr.competitor_id
    """

    df = pd.read_sql(query, conn)

    if search_name:
        df = df[
            df["competitor_name"]
            .str.contains(search_name, case=False)
        ]

    if selected_country != "All":
        df = df[df["country"] == selected_country]

    df = df[
        (df["ranking_position"] >= rank_range[0]) &
        (df["ranking_position"] <= rank_range[1])
    ]

    df = df[df["points"] >= min_points]

    df = df.reset_index(drop=True)

    st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# Competitor Details Page
elif page == "👤 Competitor Details":

    st.header("👤 Competitor Details Viewer")

    competitors = pd.read_sql("""
        SELECT competitor_name
        FROM Competitors
        ORDER BY competitor_name
    """, conn)

    selected_player = st.selectbox(
        "Select Competitor",
        competitors["competitor_name"]
    )

    details_query = f"""
    SELECT
        c.competitor_name,
        c.country,
        cr.ranking_position,
        cr.movement,
        cr.points,
        cr.competitions_played
    FROM Competitors c
    JOIN Competitor_Rankings cr
    ON c.competitor_id = cr.competitor_id
    WHERE c.competitor_name = '{selected_player}'
    """

    details = pd.read_sql(details_query, conn)

    st.table(details)


# Country Analysis Page
elif page == "🌍 Country Analysis":

    st.header("🌍 Country Wise Analysis")

    query = """
    SELECT
        c.country,
        COUNT(DISTINCT c.competitor_id) AS total_competitors,
        ROUND(AVG(cr.points),2) AS average_points
    FROM Competitors c
    JOIN Competitor_Rankings cr
    ON c.competitor_id = cr.competitor_id
    GROUP BY c.country
    ORDER BY total_competitors DESC
    """

    df = pd.read_sql(query, conn)

    st.dataframe(
        df,
        use_container_width=True,
        height=500)


    st.bar_chart(
    df.set_index("country")["total_competitors"]
)
    
# Leaderboards Page
    
elif page == "🏆 Leaderboards":

    st.header("🏆 Leaderboards")

    # Top Ranked Players
    st.subheader("🥇 Top 10 Ranked Competitors")

    query1 = """
    SELECT
        c.competitor_name,
        c.country,
        cr.ranking_position,
        cr.points
    FROM Competitors c
    JOIN Competitor_Rankings cr
    ON c.competitor_id = cr.competitor_id
    ORDER BY cr.ranking_position ASC
    LIMIT 10
    """

    top_ranked = pd.read_sql(query1, conn)

    st.dataframe(
        top_ranked,
        use_container_width=True
    )

    st.divider()

    # Highest Points Players
    st.subheader("🔥 Top 10 Competitors by Points")

    query2 = """
    SELECT
        c.competitor_name,
        c.country,
        cr.points,
        cr.ranking_position
    FROM Competitors c
    JOIN Competitor_Rankings cr
    ON c.competitor_id = cr.competitor_id
    ORDER BY cr.points DESC
    LIMIT 10
    """

    top_points = pd.read_sql(query2, conn)

    st.dataframe(
        top_points,
        use_container_width=True
    )

    st.bar_chart(
    top_points.set_index("competitor_name")["points"]
        )