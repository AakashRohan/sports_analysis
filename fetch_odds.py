from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import atexit
import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Your existing config for fetching odds
API_KEY = '5fe5ad3125788a7f7806ce5b7644fa4b'  # Replace with your actual API key
ODDS_API_URL = 'https://api.the-odds-api.com/v4/sports/{sport}/odds/'

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rohan.Aakash369",
        database="sports_analysis"
    )
    return connection

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
            INSERT INTO odds (sport, tournament, match_id, home_team, away_team, odds_home, odds_away, status, favorite, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE odds_home=VALUES(odds_home), odds_away=VALUES(odds_away), status=VALUES(status), favorite=VALUES(favorite), last_updated=CURRENT_TIMESTAMP
            """
            values = (sport_key, 'tournament_placeholder', match_id, home_team, away_team, odds_home, odds_away, status, favorite)
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

def fetch_and_update_data():
    fetch_odds()

# Schedule to fetch live data every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_update_data, trigger="interval", minutes=10)
scheduler.start()

# Schedule to fetch live data every 2 minutes for matches with real trades
scheduler.add_job(func=fetch_and_update_data, trigger="interval", minutes=2, id='real_trades_scheduler')

# Shut down the scheduler when exiting the app
atexit.register(scheduler.shutdown)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scheduler')
def scheduler():
    return render_template('scheduler.html')

@app.route('/set_scheduler', methods=['POST'])
def set_scheduler():
    duration = request.form['duration']
    sport = request.form['sport']
    match_id = request.form['match_id']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE scheduler SET duration=%s, sport=%s, match_id=%s WHERE id=1", (duration, sport, match_id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return f'Scheduler duration set to {duration} minutes for sport {sport} and match ID {match_id}'

@app.route('/current_matches')
def current_matches():
    return render_template('current_matches.html')

@app.route('/filter_matches')
def filter_matches():
    sport = request.args.get('sport', 'all')
    min_odds = request.args.get('min_odds', '0')
    status = request.args.get('status', 'all')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM odds WHERE 1=1"
    params = []

    if sport != 'all':
        query += " AND sport = %s"
        params.append(sport)
    if min_odds:
        query += " AND (odds_home >= %s OR odds_away >= %s)"
        params.append(min_odds)
        params.append(min_odds)
    if status != 'all':
        query += " AND status = %s"
        params.append(status)

    cursor.execute(query, params)
    matches = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('filtered_matches.html', matches=matches)

@app.route('/trade_management', methods=['GET'])
def trade_management():
    sport = request.args.get('sport', 'all')
    tournament = request.args.get('tournament', 'all')
    team = request.args.get('team', '')
    start_time = request.args.get('start_time', '')
    bet_type = request.args.get('bet_type', 'all')

    query = "SELECT * FROM odds WHERE 1=1"
    params = []

    if sport != 'all':
        query += " AND sport = %s"
        params.append(sport)
    if tournament != 'all':
        query += " AND tournament = %s"
        params.append(tournament)
    if team:
        query += " AND (home_team = %s OR away_team = %s)"
        params.extend([team, team])
    if start_time:
        query += " AND start_time >= %s"
        params.append(start_time)
    if bet_type != 'all':
        query += " AND bet_type = %s"
        params.append(bet_type)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    matches = cursor.fetchall()

    cursor.execute("SELECT * FROM trades")
    trades = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('trade_management.html', matches=matches, trades=trades)

@app.route('/create_trade', methods=['POST'])
def create_trade():
    sport = request.form['sport']
    tournament = request.form['tournament']
    match_id = request.form['match_id']
    team = request.form['team']
    odds = request.form['odds']
    amount = request.form['amount']
    trade_type = request.form['trade_type']
    exit_odds = request.form['exit_odds']

    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO trades (sport, tournament, match_id, team, initial_odds, amount, trade_type, exit_odds)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (sport, tournament, match_id, team, odds, amount, trade_type, exit_odds))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('trade_management'))

if __name__ == '__main__':
    app.run(debug=True)