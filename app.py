from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from config import get_db_connection

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rohan.Aakash369",
        database="sports_analysis"
    )
    return connection

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

@app.route('/trade_management')
def trade_management():
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

    cursor.execute("SELECT * FROM trades")
    trades = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('trade_management.html', matches=matches, trades=trades)

@app.route('/create_trade', methods=['POST'])
def create_trade():
    sport = request.form['sport']
    match_id = request.form['match_id']
    team = request.form['team']
    odds = request.form['odds']
    amount = request.form['amount']
    trade_type = request.form['trade_type']
    exit_odds = request.form['exit_odds']

    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO trades (sport, match_id, team, initial_odds, amount, trade_type, exit_odds)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (sport, match_id, team, odds, amount, trade_type, exit_odds))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('trade_management'))

if __name__ == '__main__':
    app.run(debug=True)