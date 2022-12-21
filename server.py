"""Server for mood share web app"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

#configuring the Flask instance.  Creating secret key to allow flash and session to work
app = Flask(__name__)
app.secret_key = "dev"
#configuring jinja2
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

#creating a route for a user profile page
@app.route("/profile")
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
@app.route("/login", methods=["POST"])
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

# Route to get all status_posts
# Calling function from crud to get all movies
@app.route('/status_posts')
def all_status_posts():
    """View all status_posts."""

    status_posts = crud.get_all_status_posts()

    return render_template('all_status_posts.html', status_posts=status_posts)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)