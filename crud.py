"""CRUD operations."""
from model import db, User, Status, Mood, connect_to_db
from datetime import datetime

def create_user(user_handle, email, password):
    """Create and return a new user."""

    user = User(user_handle=user_handle, email=email, password=password)

    return user

def create_status(user_id, status_description, post_create_date, mood_id):
    """Create and return a new mood status post."""
    print(status_description)
    status_post = Status(user_id=user_id, status_description=status_description, 
    post_create_date=post_create_date, mood_id=mood_id) 

    return status_post

def create_mood(mood_type):
    
    mood = Mood(mood_type=mood_type)

    return mood










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

