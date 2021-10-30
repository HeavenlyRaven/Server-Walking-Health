import sqlite3

database_name = "database.db"


def get_connection():
    connection = sqlite3.connect(database_name)
    connection.row_factory = sqlite3.Row
    return connection






