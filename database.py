import sqlite3
from flask import g

DATABASE = 'travel_ai.db'

print("[database.py] Database module loaded.")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        print("[database.py] Opening new database connection.")
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with sqlite3.connect(DATABASE) as db:
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("[database.py] Database initialized using schema.sql.")
