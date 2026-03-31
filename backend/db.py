import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="chandu@1602",
        database="hirematch"
    )
    return connection