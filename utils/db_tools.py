import sqlite3
from os import path

database_name = path.join(path.split(path.dirname(__file__))[0], "database.db")
IntegrityError = sqlite3.IntegrityError


def get_connection():
    connection = sqlite3.connect(database_name)
    connection.row_factory = sqlite3.Row
    return connection
