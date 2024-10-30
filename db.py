import mysql.connector

def connect_to_db():
    """Connexion à la base de données MySQL."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="toeic"
    )
    return conn
