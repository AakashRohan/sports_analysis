import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rohan.Aakash369",
        database="sports_analysis"
    )
    return connection