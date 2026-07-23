import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
load_dotenv()
class MySQLConnection:
    def __init__(self):
        self.host = os.getenv(
            "MYSQL_HOST"
        )
        self.port = int(
            os.getenv(
                "MYSQL_PORT"
            )
        )
        self.user = os.getenv(
            "MYSQL_USER"
        )
        self.password = os.getenv(
            "MYSQL_PASSWORD"
        )
        self.database = os.getenv(
            "MYSQL_DATABASE"
        )
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(
                f"MySQL connection error: {e}"
            )
            return None
if __name__ == "__main__":
    db = MySQLConnection()
    connection = db.get_connection()
    if connection:
        print(
            "Successfully connected to MySQL!"
        )
        print(
            f"Database: {db.database}"
        )
        connection.close()
    else:
        print(
            "Failed to connect to MySQL."
        )