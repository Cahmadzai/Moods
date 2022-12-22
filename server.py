"""Server for mood share web app"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime


#configuring the Flask instance.  Creating secret key to allow flash and session to work
app = Flask(__name__)
app.secret_key = "dev"
#configuring jinja2
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

# Route to get all status_posts
# Calling function from crud to get all status posts
@app.route('/status_posts')
def all_status_posts():
    """View all status_posts from all users."""

    status_posts = crud.get_all_status_posts()

    return render_template('all_status_posts.html', status_posts=status_posts)

#creating a route for a user profile page
@app.route('/profile')
def all_user_statuses():
    """A user can view all of their statuses on their profile page"""
    #if no user email == no one logged in - redirect to home
    #might not even need this? User can't get to profile page without logging in
    if "user_email" not in session:
        flash("Please log in to view your profile")
        return redirect("/login")
    else:
        user_email = session["user_email"]
        user = crud.get_user_by_email(user_email)
        user_id = user.user_id
        status_posts = crud.get_user_statuses(user_id)
        return render_template('profile.html', status_posts=status_posts) 

#Route to post a status
@app.route('/profile', methods =['POST'])
def post_a_status():
    # Using request.form because mood and description must be present to post
    # Retrieving the 'mood' and 'description' form data
    mood = request.form["mood"] 
    status_description = request.form["description"]
    #getting today's date/time
    post_create_date = datetime.now()
    #Retrieve user with matching email from session
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    #Retrieve mood value and return mood type
    mood_from_db = crud.get_mood_type(mood)
    # Creating a new status post
    new_status_post = crud.create_status(user.user_id, status_description, post_create_date, mood_from_db.mood_id)

    db.session.add(new_status_post)
    db.session.commit()
   
    flash('Your status has been posted!')
    #Might need to change this in the future so that when posting a new status
    #it stays on the page that the form is on.  This would be done through
    #Event listner, AJAX request, DOM manipulation, through front end javascript
    return redirect('/status_posts')  


#creating login page
@app.route('/login')
def login():
    return render_template('login.html')

#creating a route for account creation
@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    user_handle = request.form.get("user_handle")
    email = request.form.get("email")
    password = request.form.get("password")
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

    return redirect("/login")

#login
@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/login")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        return redirect("/")

#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)