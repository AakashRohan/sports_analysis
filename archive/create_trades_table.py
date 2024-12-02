import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rohan.Aakash369",
    database="sports_analysis"
)
cursor = conn.cursor()

# Create trades table
cursor.execute('''
CREATE TABLE IF NOT EXISTS trades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sport VARCHAR(50),
    match_id VARCHAR(50),
    team VARCHAR(50),
    odds DECIMAL(10, 2),
    amount DECIMAL(10, 2),
    trade_type VARCHAR(50),
    exit_odds DECIMAL(10, 2)
)
''')

conn.commit()
cursor.close()
conn.close()