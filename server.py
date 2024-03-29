"""Server for mood share web app"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
import os





# Configuring the Flask instance.  Creating secret key to allow flash and session to work
app = Flask(__name__)
app.secret_key = "dev"
# Configuring jinja2
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['X_RapidAPI_Key']



@app.route('/')
def homepage():
    """View homepage."""

    return redirect('/landing_page')


# Creating landing page
@app.route('/landing_page')
def landing_page():
    """A user starts on a landing page"""
    
    return render_template('landing_page.html', API_KEY = API_KEY )


# Creating a route for account creation
@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    user_handle = request.form.get("user_handle")
    email = request.form.get("email")
    password = request.form.get("password")
    print(user_handle)
    print(email)
    print(password)

    user = crud.get_user_by_email(email)
    if user:
        flash("Email already exists. Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(user_handle, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
        

    return redirect("/landing_page")

# Login
@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/landing_page")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        return redirect("/status_posts")

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/landing_page')

@app.route('/search_status_posts', methods=['GET'])
def search_status_posts():
    user_handle = request.args.get('user_handle')
    if not user_handle:
        flash('Please enter a user handle')
        return redirect('/status_posts')
    users = crud.get_users_by_handle(user_handle)
    if not users:
        flash('No user found with this handle')
        return redirect('/status_posts')
    status_posts = []
    for user in users:
        posts = crud.get_user_statuses(user.user_id)
        status_posts.extend(posts)
    return render_template('search_results.html', status_posts=status_posts)

# Route to get all status_posts
@app.route('/status_posts')
def all_status_posts():
    """View all status_posts from all users."""
    # Checks if user is logged in 
    if "user_email" not in session:
        flash("Please log in to view all status posts.")
        return redirect("/landing_page")
    else:
        # Calling function from crud to get all status posts
        status_posts = crud.get_all_status_posts()
        return render_template('all_status_posts.html', status_posts=status_posts)

# Create route for a user profile page
@app.route("/users/<user_id>")
def show_user_profile_page(user_id):
    """Show details on a particular user.""" 
    status_posts = crud.get_user_statuses(user_id)
    user = crud.get_user_by_id(user_id)
    followed_user_id = user_id
    user_email = session["user_email"]

    following_user = crud.get_user_by_email(user_email)
    if user.user_id == following_user.user_id:
        return redirect('/profile')
    following_user_id = following_user.user_id
    # Gets follow and makes sure not equal to none
    is_following = crud.get_follow(followed_user_id, following_user_id) != None
    print(is_following)

    return render_template('user_profile.html', status_posts=status_posts, user_handle=user.user_handle, is_following=is_following)

# Creating a route for a user profile page
@app.route('/profile')
def all_user_statuses():
    """A user can view all of their statuses on their profile page"""
    # If no user email == no one logged in - redirect to home
    # Might not even need this? User can't get to profile page without logging in
    if "user_email" not in session:
        flash("Please log in to view your profile.")
        return redirect("/landing_page")
    else:
        user_email = session["user_email"]
        user = crud.get_user_by_email(user_email)
        user_id = user.user_id
        status_posts = crud.get_user_statuses(user_id)
        return render_template('profile.html', status_posts=status_posts) 

# Route to view all followed users and their statuses
@app.route('/following')
def all_following():
    """View all followed users and their statuses"""
    # Checks if user is logged in 
    if "user_email" not in session:
        flash("Please log in to view users you follow.")
        return redirect("/landing_page")
    else:
        user_email = session["user_email"]
        user = crud.get_user_by_email(user_email)
        # Gets list of followed users and pass in user_id
        followed_users = crud.get_users_followed(user.user_id)
        # Pass in followed users to be displayed in template
        status_posts = []
        for followed_user in followed_users:
            status_posts.append(followed_user.status_posts)

        return render_template('all_following.html', followed=followed_users, status_posts=status_posts, user_handle=user.user_handle)

# Follow route
@app.route('/follow', methods=['POST'])
def follow():
    """Follow a user"""
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    following_user_id = user.user_id

    followed_user_handle = request.form.get('follow_user_handle')
    followed_user = crud.get_user_by_handle(followed_user_handle)
    followed_user_id = followed_user.user_id
    is_following = crud.get_follow(followed_user_id, following_user_id) != None

    if is_following:
        flash(f'You are already following {followed_user.user_handle}.')
        return redirect('/following')
    
    elif crud.create_follow(followed_user_id, following_user_id):
        flash(f'You are now following {followed_user.user_handle}.')
        print(f'You are now following {followed_user.user_handle}.')
        return redirect('/following')
         
    else:
        flash('An error has occured.  Unable to follow user.')
        return redirect('/following') 

# Unfollow route
@app.route('/unfollow', methods=['POST'])
def unfollow():
    """Unfollow a user"""
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    following_user_id = user.user_id

    followed_user_handle = request.form.get('unfollow_user_handle')
    print(followed_user_handle)
    followed_user = crud.get_user_by_handle(followed_user_handle)
    print(followed_user.user_handle)
    followed_user_id = followed_user.user_id

    if crud.create_unfollow(followed_user_id, following_user_id):

        flash(f'You have unfollowed {followed_user.user_handle}.')
        print(f'You have unfollowed {followed_user.user_handle}.')
        return redirect('/following')
        
    else:
        flash('An error has occured.  Unable to unfollow user.')
        return redirect('/following')


#Route to post a status
@app.route('/profile', methods =['POST'])
def post_a_status():
    """Post a status"""
    # Using request.form because mood and description must be present to post
    # Retrieving the 'mood' and 'description'form data
    mood = request.form.get("mood") 
    status_description = request.form.get("description")
    # Getting today's date/time
    post_create_date = datetime.now()
    # Retrieve user with matching email from session
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    # Retrieve mood value and return mood type
    mood_from_db = crud.get_mood_type(mood)
    # Creating a new status post
    new_status_post = crud.create_status(user.user_id, status_description, post_create_date, mood_from_db.mood_id)

    db.session.add(new_status_post)
    db.session.commit()
   
    flash('Your status has been posted!')
    #Might need to change this in the future so that when posting a new status
    #it stays on the page that the form is on.  This would be done through
    #Event listner, AJAX request, DOM manipulation, through front-end javascript
    return redirect('/status_posts') 


#Route to post a comment
@app.route('/post_a_comment', methods =['POST'])
def post_a_comment():
    comment_description = request.form.get("comment-description")
    status_id = request.form.get("status-id")
    post_create_date = datetime.now()
   
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    
    new_comment = crud.create_comment(user.user_id, status_id, comment_description,post_create_date)

    db.session.add(new_comment)
    db.session.commit()

    flash('Your comment has been posted!')
    return redirect ('/status_posts')



# Delete a status
# Int tells Flask to expect integer value for the status_id
# If I just use <status_id> would treat URL parameter as string
@app.route('/delete-status/<int:status_id>', methods=['POST'])
def delete_status(status_id):
    """Delete a status by id."""
    if crud.delete_status(status_id):
        flash("Status deleted.")
    else:
        flash("There was an error when trying to delete your status. Please try again")
        # Use AJAX to fix these redirects and stay on page without reloading
    return redirect("/profile")

@app.route('/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    """Delete a comment by id"""
    if crud.delete_comment(comment_id):
        flash("Comment deleted.")
    else:
        flash("There was an error when trying to delete your comment. Please try again")
    return redirect("/profile")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)