import sqlite3

database_name = "database.db"
IntegrityError = sqlite3.IntegrityError


def get_connection():
    connection = sqlite3.connect(database_name)
    connection.row_factory = sqlite3.Row
    return connection






