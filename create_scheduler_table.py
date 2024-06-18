import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rohan.Aakash369",
    database="sports_analysis"
)
cursor = conn.cursor()

# Modify scheduler table to add sport and match_id columns
cursor.execute('''
ALTER TABLE scheduler
ADD COLUMN sport VARCHAR(255),
ADD COLUMN match_id VARCHAR(255)
''')

# Insert default value
cursor.execute("INSERT INTO scheduler (id, duration, sport, match_id) VALUES (1, 10, 'all', 'all') ON DUPLICATE KEY UPDATE id=id")

conn.commit()
cursor.close()
conn.close()