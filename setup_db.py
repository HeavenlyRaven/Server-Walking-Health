from utils.db_tools import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.executescript("""
CREATE TABLE users (
login TEXT PRIMARY KEY, 
password TEXT NOT NULL, 
fullname TEXT NOT NULL, 
doctorLogin TEXT, 
stepLength REAL, 
FOREIGN KEY (doctorLogin) REFERENCES users (login)
);
CREATE TABLE messages (
doctorLogin TEXT NOT NULL, 
patientLogin TEXT NOT NULL, 
message TEXT NOT NULL, 
timestamp INTEGER NOT NULL, 
FOREIGN KEY (doctorLogin, patientLogin) REFERENCES users (doctorLogin, login)
);
CREATE TABLE data (
date TEXT NOT NULL, 
login TEXT NOT NULL,
timestamp INTEGER NOT NULL, 
acceleration REAL NOT NULL, 
distance REAL NOT NULL, 
speed REAL NOT NULL, 
PRIMARY KEY (date, login, timestamp), 
FOREIGN KEY (login) REFERENCES users (login)
)""")

connection.commit()
connection.close()
