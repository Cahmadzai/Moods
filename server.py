"""Server for mood share web app"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
import os





#configuring the Flask instance.  Creating secret key to allow flash and session to work
app = Flask(__name__)
app.secret_key = "dev"
#configuring jinja2
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['X_RapidAPI_Key']



@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


#creating landing page
@app.route('/landing_page')
def landing_page():
    """A user starts on a landing page"""
    
    return render_template('landing_page.html', API_KEY = API_KEY )

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



@app.route('/search_status_posts', methods=['GET'])
def search_status_posts():
    user_handle = request.args.get('user_handle')
    #print(f"this is user_handle **** {user_handle}")
    if not user_handle:
        flash('Please enter a user handle')
        return redirect('/status_posts')
    users = crud.get_users_by_handle(user_handle)
    #print(f"this is users**** {users}")
    if not users:
        flash('No user found with this handle')
        return redirect('/status_posts')
    status_posts = []
    for user in users:
        posts = crud.get_user_statuses(user.user_id)
        status_posts.extend(posts)
        #print(f"this is status posts **** {status_posts}")
    return render_template('search_results.html', status_posts=status_posts)


# Route to get all status_posts
# Calling function from crud to get all status posts
@app.route('/status_posts')
def all_status_posts():
    """View all status_posts from all users."""
    #checks if user is logged in 
    if "user_email" not in session:
        flash("Please log in to view all status posts.")
        return redirect("/login")
    else:
        status_posts = crud.get_all_status_posts()
        return render_template('all_status_posts.html', status_posts=status_posts)

#create route for a user profile page
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
    #gets follow and makes sure not equal to none
    is_following = crud.get_follow(followed_user_id, following_user_id) != None
    print(is_following)
    # user_email = session["user_email"]

    return render_template('user_profile.html', status_posts=status_posts, user_handle=user.user_handle, is_following=is_following)


#creating a route for a user profile page
@app.route('/profile')
def all_user_statuses():
    """A user can view all of their statuses on their profile page"""
    #if no user email == no one logged in - redirect to home
    #might not even need this? User can't get to profile page without logging in
    if "user_email" not in session:
        flash("Please log in to view your profile.")
        return redirect("/login")
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
    #checks if user is logged in 
    if "user_email" not in session:
        flash("Please log in to view users you follow.")
        return redirect("/login")
    else:
        user_email = session["user_email"]
        user = crud.get_user_by_email(user_email)
        #gets list of followed users and pass in user_id
        followed_users = crud.get_users_followed(user.user_id)
        #pass in followed users to be displayed in template
        status_posts = []
        for followed_user in followed_users:
            status_posts.append(followed_user.status_posts)

        return render_template('all_following.html', followed=followed_users, status_posts=status_posts, user_handle=user.user_handle)

#follow route
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

#unfollow route
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


#Route to post a comment
@app.route('/post_a_comment', methods =['POST'])
def post_a_comment():
    #change to request.form.get
    comment_description = request.form["comment-description"]
    status_id = request.form["status-id"]
    post_create_date = datetime.now()
   
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    
    new_comment = crud.create_comment(user.user_id, status_id, comment_description,post_create_date)

    db.session.add(new_comment)
    db.session.commit()

    flash('Your comment has been posted!')
    return redirect ('/status_posts')



#delete a status
#int tells Flask to expect integer value for the status_id
#if just use <status_id> would treat URL parameter as string
@app.route('/delete-status/<int:status_id>', methods=['POST'])
def delete_status(status_id):
    """Delete a status by id."""
    #may want to add authorization checks to make sure only user that
    #posted status can delete (come back to this)
    if crud.delete_status(status_id):
        flash("Status deleted.")
    else:
        flash("There was an error when trying to delete your status. Please try again")
        #I might need to use AJAX to fix these redirects and stay on page without reloading
    return redirect("/profile")

@app.route('/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    """Delete a comment by id"""
    if crud.delete_comment(comment_id):
        flash("Comment deleted.")
    else:
        flash("There was an error when trying to delete your comment. Please try again")
    return redirect("/status_posts")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)