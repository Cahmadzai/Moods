"""Script to seed database"""
import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb model')
os.system('createdb model')

model.connect_to_db(server.app)
model.db.create_all()

# create fake users here
# grab user ids here

# create fake moods here
# grab mood ids here

#Load status posts data from JSON file
with open('data/status_posts.json') as f:
    status_post_data = json.loads(f.read())

# Create status posts, store them in list so we can use them
# to create fake moods later
status_posts_in_db = []

for status_posts in status_post_data:
    # get the user_handle, status_description, and mood_type from the status post.
    user_handle,status_description,mood_type = (
        status_posts['user_handle'],
        status_posts['status_description'],
        status_posts['mood_type'],
        # status_posts['mood_id'],
        # status_posts['user_id'],
        )
    # dictionary. Then, get the post_create_date and convert it to a
    # datetime object with datetime.strptime
    post_create_date = datetime.now() # datetime.strptime(status_posts["post_create_date"], "%Y-%m-%d-%H")
    print(post_create_date)

    # create a status here and append it to status_posts_in_db
    db_status_post = crud.create_status(user_id, status_description, post_create_date, mood_id)
    status_posts_in_db.append(db_status_post)

    model.db.session.add_all(status_posts_in_db)
    model.db.session.commit()







