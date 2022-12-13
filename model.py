"""Models for mood sharing website."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_handle = db.Column(db.String(25), unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} user_handle={self.user_handle} email={self.email}>'

class Status(db.Model):
    """A mood status post."""

    __tablename__ = "status posts"

    status_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    status_id_description = db.Column(db.String(255))
    post_create_date = db.Column(db.DateTime)
    mood_id = db.Column(db.Integer, db.ForeignKey("moods.mood_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f'<Status status_id={self.status_id} status_id_description={self.status_id_description} post_create_date{self.post_create_date}>'

class Mood(db.Model):
    """A mood type."""

    __tablename__ = "moods"

    mood_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    mood_type = db.Column(db.String)

    def __repr__(self):
        return f'<Mood mood_id={self.mood_id} mood_type={self.mood_type}>'