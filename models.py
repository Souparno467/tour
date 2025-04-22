from flask_login import UserMixin
from database import get_db

print("[models.py] Models module loaded.")

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

def get_user_by_id(user_id):
    db = get_db()
    user = db.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        return User(user['id'], user['username'], user['email'])
    return None

class Trip:
    @staticmethod
    def save_trip(user_id, destination, itinerary):
        db = get_db()
        db.execute("INSERT INTO trips (user_id, destination, itinerary) VALUES (?, ?, ?)", (user_id, destination, itinerary))
        db.commit()

def get_user_trips(user_id):
    db = get_db()
    trips = db.execute("SELECT * FROM trips WHERE user_id = ?", (user_id,)).fetchall()
    return trips if trips else []  # Ensuring an empty list instead of None
