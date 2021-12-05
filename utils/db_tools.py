import sqlite3

database_name = "Server-Walking-Health/database.db"
IntegrityError = sqlite3.IntegrityError


def get_connection(with_row_names=True):
    connection = sqlite3.connect(database_name)
    if with_row_names:
        connection.row_factory = sqlite3.Row
    return connection
