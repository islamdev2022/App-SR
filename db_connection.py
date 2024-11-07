import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        print("Attempting to connect...")
        connection = mysql.connector.connect(
            host="localhost",        
            user="root",     
            password="", 
            database="app-sr" 
        )
        if connection.is_connected():
            print("Connection to MySQL was successful")
            return connection
    except Error as e:
        print(f"Error: '{e}' occurred")
        return None
