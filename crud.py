"""CRUD operations."""
from model import db, User, Status, Mood,Comment, Follow,  connect_to_db
from datetime import datetime
from sqlalchemy import func

def create_user(user_handle, email, password):
    """Create and return a new user."""

    user = User(user_handle=user_handle, email=email, password=password)

    return user


#create follow
def create_follow(followed_user_id, following_user_id):
    """Follow a user."""

    follow = Follow(followed_user_id=followed_user_id, following_user_id=following_user_id)

    if follow:
        db.session.add(follow)
        db.session.commit()
        return follow

#create unfollow
def create_unfollow(followed_user_id, following_user_id):
    """Unfollow a user."""
    follow = get_follow(followed_user_id, following_user_id)
    print(f'You have unfollowed {follow}.')
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return True
    else:
        return False

    # follow.is_active = False
    #     db.session.commit()
    #     return True
    # else:
    #     return False

def create_status(user_id, status_description, post_create_date, mood_id):
    """Create and return a new mood status post."""
    status_post = Status(user_id=user_id, status_description=status_description, 
    post_create_date=post_create_date, mood_id=mood_id) 

    return status_post

def create_comment(user_id, status_id, comment_description,post_create_date):
    """Create and return a new comment"""
    comment = Comment(user_id=user_id, status_id=status_id, comment_description=comment_description, post_create_date=post_create_date)

    return comment

#get follow
def get_follow(followed_user_id, following_user_id):
    """Get a follow."""
    #using SQLAlchemy to  execute query database.
    #filtering results by followed_user_id and following_user_id columns
    follow = Follow.query.filter(Follow.followed_user_id == followed_user_id, Follow.following_user_id == following_user_id).first()
    
    return follow
 
def get_users_followed(user_id):
    """Return followed users and their statuses"""
    # follows represents users that user_id is following
    # returns Follow objects where following_user_id field is equal to user id paramater passed in 
    follows = Follow.query.filter_by(following_user_id=user_id).all()
    followed_user_id_list = []
    for follow in follows:
        followed_user_id_list.append(follow.followed_user_id)
    print(followed_user_id_list)

    #finding all users whose user_id is in followed_user_id_list and storing in followed_users
    followed_users = User.query.filter(User.user_id.in_(followed_user_id_list)).all()
    #statuses = Status.query.filter(Status.user_id.in_(followed_user_id_list)).all()

    return followed_users

def get_all_users():
    """Return all users."""
    return User.query.all()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user by id."""

    return User.query.filter(User.user_id == user_id).first()

def get_status_by_id(status_id):
    """Return a status by id."""

    return Status.query.filter(Status.status_id == status_id).first()


def get_user_by_handle(user_handle):
    """Return a user by handle."""

    return User.query.filter(User.user_handle == user_handle).first()

def get_users_by_handle(user_handle):
    """Return a list of users by handle."""
    #using func.lower from sqlalchemy to make search case insensitive
    #changes user handle stored in database by making it lower case and compares to search
    return User.query.filter(func.lower(User.user_handle).contains(user_handle.lower())).all()

def get_user_statuses(user_id):
    """Return statuses for one user on their profile page"""
    #double check this, might be adding time expiration in the future or date separation
    return Status.query.filter(Status.user_id == user_id).all()


def get_comments(status_id):
    """Return all comments for each status post by different users"""

    comments = Comment.query.filter(Comment.status_id == status_id ).all()

    return comments

def get_all_status_posts():
    """Return all status posts."""
    return Status.query.order_by(Status.post_create_date).all()

def create_mood(mood_type):

    mood = Mood(mood_type=mood_type)

    return mood

def get_mood_type(mood_type):
    """Returns the mood for a given mood type"""
    return Mood.query.filter(Mood.mood_type == mood_type).first()


def delete_status(status_id):
    """Delete a status by id."""
    status = Status.query.filter(Status.status_id == status_id).first()
    if status:
        db.session.delete(status)
        db.session.commit()
        return True
    else:
        return False

def delete_comment(comment_id):
    """Delete a comment by id."""
    comment = Comment.query.filter(Comment.comment_id == comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return True
    else:
        return False

















if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    #db.drop_all()
    # db.create_all()

    # user= create_user(user_handle='user123', email='test@gmail.com', password='test1234')
    # mood= create_mood(mood_type='happy')
    # status= create_status(user.user_id, 'teststatus', datetime.now(), mood.mood_id)
    # db.session.add_all([user, mood, status])
    # db.session.commit()
    # print(user, mood, status)

