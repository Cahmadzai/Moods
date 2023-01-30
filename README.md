![Mpath logo!](https://github.com/Cahmadzai/Moods/blob/a52dd31759c2276041d23cd00669e4d8919e03a7/static/images/logo.png)

# Mpath

## Summary
Mpath is a platform that empowers users to express and connect with others by sharing their moods and thoughts.  Many platforms revolve around sharing what is happening with us on the outside.  We often share the latest travel or maybe what we are eating for lunch today, but we hardly let others know how we are feeling and why.  I was inspired to make Mpath to help us share what’s happening within.  

## About the developer

Mpath was created by Christina Ahmadzai a software engineer in California.  Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/christina-ahmadzai/).

## Technologies

### Tech stack
<ul>
  <li>Python3</li>
  <li>PostgreSQL</li>
  <li>SQLAlchemy</li>
  <li>Jinja</li>
  <li>Quote API</li>
  <li>Bootstrap</li>
  <li>Javascript</li>
  <li>HTML</li>
  <li>CSS</li>
  <li>JSON</li>
  <li>AJAX</li>
</ul>

Mpath is built on a SQL database that uses SQLAlchemy for database management in Python3. The server is created using Flask and the front-end design of Mpath was built using a combination of the Flask web framework, SQLAlchemy, Jinja templating, CSS and the bootstrap framework.  The quote of the day located on the landing page of Mpath was implemented using AJAX to make a GET request to an external API.  

## Features
![Landing page!](https://github.com/Cahmadzai/Moods/blob/a52dd31759c2276041d23cd00669e4d8919e03a7/static/images/landingpage.png)
![Homepage!](https://github.com/Cahmadzai/Moods/blob/a52dd31759c2276041d23cd00669e4d8919e03a7/static/images/homepage.png)

At Mpath's homepage, users can view the latest mood updates posted by others. They can show support by commenting on a mood update, or they can create their own mood update by choosing a mood from the dropdown menu, describing their feelings in the text box, and submitting the form.

![Search results!](https://github.com/Cahmadzai/Moods/blob/a52dd31759c2276041d23cd00669e4d8919e03a7/static/images/search.png)

Users can search for specific users on the platform by entering a user handle into the search bar. The server will search the database for any matching handles and display the results on a separate search results page. For example, if a user types "Martin" into the search bar, the results will display all user handles similar to "Martin".

![Follow and unfollow!](https://github.com/Cahmadzai/Moods/blob/a52dd31759c2276041d23cd00669e4d8919e03a7/static/images/follow.png)

The user's profile page features Jinja logic that displays either a "follow" or "unfollow" button based on the viewing user's relationship with the viewed user. If the viewing user decides to follow another user, they can see a list of all the users they follow and their related status posts on their "following" page.

## Version 2.0

I plan to...
<ul>
  <li> Better the user experience by using AJAX to prevent full page reloads</li>
  <li>Enable users to engage in more discussions by adding threaded replies</li>
  <li>Ensure more security of user data by implementing password hashing
</li>
</ul>















