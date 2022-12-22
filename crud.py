"""CRUD operations."""
from model import db, User, Status, Mood, connect_to_db
from datetime import datetime

def create_user(user_handle, email, password):
    """Create and return a new user."""

    user = User(user_handle=user_handle, email=email, password=password)

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_statuses(user_id):
    """Return statuses for one user on their profile page"""
    #double check this, might be adding time expiration in the future or date separation
    return Status.query.filter(Status.user_id == user_id).all()

def create_status(user_id, status_description, post_create_date, mood_id):
    """Create and return a new mood status post."""
    status_post = Status(user_id=user_id, status_description=status_description, 
    post_create_date=post_create_date, mood_id=mood_id) 

    return status_post

def get_all_status_posts():
    """Return all status posts."""
    return Status.query.all()

def create_mood(mood_type):

    mood = Mood(mood_type=mood_type)

    return mood

def get_mood_type(mood_type):
    """Returns the mood for a given mood type"""
    return Mood.query.filter(Mood.mood_type == mood_type).first()














if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    # db.drop_all()
    # db.create_all()

    # user= create_user(user_handle='user123', email='test@gmail.com', password='test1234')
    # mood= create_mood(mood_type='happy')
    # status= create_status(user.user_id, 'teststatus', datetime.now(), mood.mood_id)
    # db.session.add_all([user, mood, status])
    # db.session.commit()
    # print(user, mood, status)

