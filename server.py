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


# Route to get all status_posts
# Calling function from crud to get all movies
@app.route("/status_posts")
def all_status_posts():
    """View all status_posts."""

    status_posts = crud.get_all_status_posts()

    return render_template("all_status_posts.html", status_posts=status_posts)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)