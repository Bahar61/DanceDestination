"""Dance Destination."""

from pprint import pformat
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash, session
from model import User, Event, UserEvent, connect_to_db, db
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

    # Get from variables.
    genre = request.args.get('genre')
    location = request.args.get('location') or 'San Francisco'
    distance = request.args.get('distance') or 25
    measurement = request.args.get('measurement')
    sort = request.args.get('sort')
          
    # If the required information is in the request, look for event
    if genre and (location and distance and measurement):

        # The Eventbrite API requires the location.within value to have the
        # distance measurement as well
        within = f'{distance}{measurement}'

        payload = {'q': f'{genre} dance', # Add dance to genre for Eventbrite search
                   'location.address': location,
                   'location.within': within,
                   'sort_by': sort,
                   }

        #Eventbrite API access and authentication 
        base_url = 'https://www.eventbriteapi.com/v3'
        token = os.environ.get('EVENTBRITE_TOKEN') 
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(f'{base_url}/events/search', params=payload, headers=headers)
        data = response.json()
        elect_events = []

        # If genre is Electronic pull data from database where 19hz website results is saved.
        if genre == 'Electronic':
            elect_events = Event.query.all() 


        # If the response was successful use the list of events from the returned JSON
        if response.ok:
            events = data['events']

        # If there was an error (status code between 400 and 600), use an empty list
        else:
            flash(f"No events: {data['error_description']}")
            events = []
        

        return render_template("events.html",
                               data=pformat(data),
                               eventbrite_results=events,
                               elect_results=elect_events,
                               genre=genre,
                               )

    # If the required info isn't in the request, redirect to the search form
    else:
        flash("Please Enter All Required Information!")
        
        return redirect("/")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")



@app.route('/register', methods=['POST'])
def register_process():
    """Process registration and add new user to database."""

    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']    

    user = User.query.filter_by(email=email).first()

    if email == user.email:
        flash("We have danced before! Please Log In!")
        return redirect("/register")
    else:
        new_user = User(fname=fname, lname=lname, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        
        session['user_id'] = user.user_id

        flash(f"{user.fname} Welcome! Shall we dance?.")
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
        flash("We haven't danced yet!")
        return redirect("/login")

    if user.password != password:
        print(user.password)
        flash("Last time you didn't use this password!")
        return redirect("/login")

    session['user_id'] = user.user_id

    flash(f"{user.fname} shall we dance again?")
    return redirect(f"/")



@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash(f"You are already missed! Please come back!")
    return redirect("/")
  


@app.route('/about')
def about():
    """Homepage."""

    return render_template("about.html")


if __name__ == "__main__":
    # set debug=True here, to invoke the DebugToolbarExtension 
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.config['SECRET_KEY'] = "<Something I don't want you to guess!>"

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

