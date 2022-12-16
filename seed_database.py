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
# user_ids = []

#Load users data from JSON file
with open('data/users.json') as f:
    users_data = json.loads(f.read())
    #created empty list 
    users_in_db = []
    for user in users_data:
        user_handle, email, password = (
            user['user_handle'],
            user['email'],
            user['password'],
        )
        db_user = crud.create_user(user_handle, email, password)
        users_in_db.append(db_user)
    
    model.db.session.add_all(users_in_db)
    model.db.session.commit()


# create fake moods here
# grab mood ids here
with open('data/moods.json') as f:
    moods_data = json.loads(f.read())
    moods_in_db = []
    for mood in moods_data:
        mood_type = mood['mood_type']
    
        db_mood = crud.create_mood(mood_type)
        moods_in_db.append(db_mood)
    
    model.db.session.add_all(moods_in_db)
    model.db.session.commit()


#Load status posts data from JSON file
with open('data/status_posts.json') as f:
    status_post_data = json.loads(f.read())

# Create status posts, store them in list so we can use them
# to create fake moods later
status_posts_in_db = []

for status_posts in status_post_data:
    # get the user_handle, status_description, and mood_type from the status post.
    status_description = status_posts['status_description']
        # status_posts['mood_type'],
        # status_posts['mood_id'],
        # status_posts['user_id'],
    
    # dictionary. Then, get the post_create_date and convert it to a
    # datetime object with datetime.strptime
    post_create_date = datetime.now() # datetime.strptime(status_posts["post_create_date"], "%Y-%m-%d-%H")
   

    #pulling random user id and mood id from users created in db
    random_user_id = choice(users_in_db).user_id
    random_mood_id = choice(moods_in_db).mood_id
    # create a status here and append it to status_posts_in_db
    db_status_post = crud.create_status(random_user_id, status_description, post_create_date, random_mood_id)
    status_posts_in_db.append(db_status_post)

model.db.session.add_all(status_posts_in_db)
model.db.session.commit()







