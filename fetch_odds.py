import time
import requests
import json
import logging
from config import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = '5fe5ad3125788a7f7806ce5b7644fa4b'
ODDS_API_URL = 'https://api.the-odds-api.com/v4/sports/{sport}/odds/'

def fetch_odds():
    logging.info("Fetching odds data...")
    sports = ['cricket', 'soccer', 'tennis']
    for sport in sports:
        response = requests.get(ODDS_API_URL.format(sport=sport), params={
            'apiKey': API_KEY,
            'regions': 'us',
            'markets': 'h2h'
        })
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Fetched {len(data)} matches for {sport}.")
            store_odds(data, sport)
        else:
            logging.error(f"Failed to fetch data for {sport}. Status code: {response.status_code}")

def store_odds(odds, sport):
    logging.info("Storing odds data in the database...")
    connection = get_db_connection()
    cursor = connection.cursor()

    for match in odds:
        try:
            sport_key = sport
            match_id = match['id']
            home_team = match['home_team']
            away_team = match['away_team']
            odds_home = match['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            odds_away = match['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
            status = 'prematch'  # Assuming initial status as 'prematch'
            favorite = home_team if odds_home < odds_away else away_team
            
            query = """
            INSERT INTO odds (sport, match_id, home_team, away_team, odds_home, odds_away, status, favorite)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE odds_home=VALUES(odds_home), odds_away=VALUES(odds_away), status=VALUES(status), favorite=VALUES(favorite)
            """
            values = (sport_key, match_id, home_team, away_team, odds_home, odds_away, status, favorite)
            cursor.execute(query, values)
            logging.info(f"Inserted/Updated odds for match {match_id}.")
        except KeyError as e:
            logging.error(f"Key error: {e} in match: {match}")

    connection.commit()
    cursor.close()
    connection.close()
    logging.info("Finished storing odds data.")

def update_scheduler():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch matches with active trades
    cursor.execute("SELECT DISTINCT match_id FROM trades WHERE trade_type='Real' AND outcome IS NULL")
    active_matches = cursor.fetchall()

    # Update scheduler intervals based on active trades
    for match in active_matches:
        cursor.execute("UPDATE scheduler SET interval=2 WHERE match_id=%s", (match['match_id'],))
    
    # Reset intervals for matches without active trades
    cursor.execute("UPDATE scheduler SET interval=10 WHERE match_id NOT IN (SELECT DISTINCT match_id FROM trades WHERE trade_type='Real' AND outcome IS NULL)")
    
    connection.commit()
    cursor.close()
    connection.close()

def run_scheduler():
    while True:
        update_scheduler()
        fetch_odds()
        time.sleep(600)  # Default 10 minutes interval

if __name__ == "__main__":
    run_scheduler()