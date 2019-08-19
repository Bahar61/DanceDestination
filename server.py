"""Dance Destination."""

from pprint import pformat
from jinja2 import StrictUndefined 
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash, session, redirect
from model import User, Event, Genre, UserEvent, EventGenre, connect_to_db, db
import requests
import os
import json


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "Something I don't want you to guess!"

#if an undefined variable used in Jinja2, raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Homepage."""

    return render_template("dance_destination.html")



@app.route('/events', methods=['GET'])
def search_event():
    """Search for event."""


    genres = request.args.getlist('genre')
    location = request.args.get('location')
    distance = request.args.get('distance')
    measurement = request.args.get('measurement')
    sort = request.args.get('sort')


    # loop through genre list and add 'dance' to each
    query = []
    for genre in genres:
        query.append(f'{genre} dance')
    

    # If the required information is in the request, look for event
    if genre or (location and distance and measurement):

        # The Eventbrite API requires the location.within value to have the
        # distance measurement as well
        distance = distance + measurement

        payload = {'q': ', '.join(query),
                   'location.address': location,
                   'location.within': distance,
                   'sort_by': sort,
                   }

        
        base_url = 'https://www.eventbriteapi.com/v3'
        token = os.environ.get('EVENTBRITE_TOKEN') 
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(f'{base_url}/events/search', params=payload, headers=headers)
        data = response.json()
        print('\n\n\n\n\n\n\n')
        print(response.url)
        

        # If the response was successful (with a status code of less than 400),
        # use the list of events from the returned JSON
        if response.ok:
            events = data['events']
            
        # If there was an error (status code between 400 and 600), use an empty list
        else:
            flash(f"No events: {data['error_description']}")
            events = []

        return render_template("events.html",
                               data=pformat(data),
                               results=events)

    # If the required info isn't in the request, redirect to the search form
    else:
        flash("Please enter all required information!")
        return redirect("/")



@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")



@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']    

    new_user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"{fname} welcome to DanceDestination.")
    return redirect("/")



@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")



@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("This email is not registered!")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session['user_id'] = user.user_id

    flash("Logged in")
    return redirect(f"/users/{user.user_id}")



@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash("Logged Out.")
    return redirect("/")
  


# @app.route("/events")
# def show_events():
#     """Show info about events."""

#     # event_query = Event.query


    # # check for parameters
    # genre = request.args.get('genre')
    # location = request.args.get('location')
    # date = request.args.get('date')
    


    # # check the users input and pass it to the API request
    # if location:
    #     event_query = event_query.filter_by(location=location)

    # if genre:
    #     event_query = event_query.filter_by(genres=genres)

    # if date:
    #     event_query = event_query.filter_by(date=date)


    # events = event_query.all()
    # print(event_query)

    # return render_template("events.html", events=events)





@app.route('/about')
def about():
    """Homepage."""
    return render_template("about.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.config['SECRET_KEY'] = "<Something I don't want you to guess!>"

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')