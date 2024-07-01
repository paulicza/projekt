from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reservations = db.relationship('Reservation', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    menu = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    reservations = db.relationship('Reservation', backref='restaurant', lazy=True)

    def __repr__(self):
        return f"Restaurant('{self.name}', '{self.location}', '{self.capacity}')"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    menu_choice = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Reservation('{self.date}', '{self.guests}', '{self.menu_choice}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))