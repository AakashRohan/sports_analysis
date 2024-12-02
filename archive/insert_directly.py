import requests
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rohan.Aakash369",
        database="sports_analysis"
    )

# Insert match data
def insert_match_data(match):
    conn = get_db_connection()
    cursor = conn.cursor()

    match_id = match['id']
    sport_key = match['sport_key']
    sport_title = match['sport_title']
    commence_time = datetime.fromisoformat(match['commence_time'].replace('Z', ''))
    home_team = match['home_team']
    away_team = match['away_team']

    cursor.execute("""
        INSERT INTO matches (id, sport_key, sport_title, commence_time, home_team, away_team)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        sport_key = VALUES(sport_key),
        sport_title = VALUES(sport_title),
        commence_time = VALUES(commence_time),
        home_team = VALUES(home_team),
        away_team = VALUES(away_team)
    """, (match_id, sport_key, sport_title, commence_time, home_team, away_team))

    conn.commit()
    cursor.close()
    conn.close()

# Insert odds data
def insert_odds_data(match):
    conn = get_db_connection()
    cursor = conn.cursor()

    match_id = match['id']
    for bookmaker in match['bookmakers']:
        bookmaker_key = bookmaker['key']
        bookmaker_title = bookmaker['title']
        last_update = datetime.fromisoformat(bookmaker['last_update'].replace('Z', ''))

        for market in bookmaker['markets']:
            market_key = market['key']
            for outcome in market['outcomes']:
                team_name = outcome['name']
                price = outcome['price']

                cursor.execute("""
                    INSERT INTO bookmaker_odds (match_id, bookmaker_key, bookmaker_title, last_update, market_key, team_name, price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (match_id, bookmaker_key, bookmaker_title, last_update, market_key, team_name, price))

    conn.commit()
    cursor.close()
    conn.close()

# Fetch and insert data from API
def fetch_and_insert_data():
    API_KEY = os.getenv('ODDS_API_KEY')
    # Use EU region to get all bookmakers
    url = f'https://api.the-odds-api.com/v4/sports/cricket_test_match/odds/?apiKey={API_KEY}&regions=eu&markets=h2h'
    
    response = requests.get(url)
    if response.status_code == 200:
        matches = response.json()
        for match in matches:
            # Debug: Print available bookmakers
            print("Match:", match['home_team'], "vs", match['away_team'])
            print("Available bookmakers:", [b['key'] for b in match['bookmakers']])
            print("---")
            
            insert_match_data(match)
            insert_odds_data(match)
        print("Data inserted successfully.")
    else:
        print(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    fetch_and_insert_data() 