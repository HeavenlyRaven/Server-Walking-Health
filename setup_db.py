from utils.db_tools import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.executescript("""
CREATE TABLE users (
id INTEGER PRIMARY KEY,
login TEXT UNIQUE NOT NULL, 
password TEXT, 
fullname TEXT NOT NULL, 
doctorId INTEGER, 
stepLength REAL,
token TEXT UNIQUE NOT NULL, 
FOREIGN KEY (doctorId) REFERENCES users (id)
);
CREATE TABLE messages (
doctorId INTEGER NOT NULL, 
patientId INTEGER NOT NULL, 
message TEXT NOT NULL, 
timestamp INTEGER NOT NULL, 
FOREIGN KEY (doctorId, patientId) REFERENCES users (doctorId, id)
);
CREATE TABLE data (
date TEXT NOT NULL, 
id TEXT NOT NULL,
timestamp INTEGER NOT NULL, 
acceleration REAL NOT NULL, 
distance REAL NOT NULL, 
speed REAL NOT NULL, 
PRIMARY KEY (date, id, timestamp), 
FOREIGN KEY (id) REFERENCES users (id)
)""")

connection.commit()
connection.close()
