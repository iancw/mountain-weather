import sqlite3

db_file = 'weather.db'

def create_tables():
	conn=sqlite3.connect(db_file)
	c=conn.cursor()
	c.execute('''CREATE TABLE measurement (day date, hour int, duration int, low real, high real)''')

def add_record(grb):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()

