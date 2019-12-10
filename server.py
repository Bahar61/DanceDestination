"""Dance Destination."""

from pprint import pformat
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash, session
from model import User, Event, UserEvent, connect_to_db, db
import requests
import os
import json
import bleach
import logging

#setup basic config for logging
logging.basicConfig(filename='test.log', level=logging.INFO, 
    format='[%(asctime)s] [%(levelname)s] %(message)s')


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get('MySecretServerKey')

#if an undefined variable used in Jinja2, raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Homepage."""

    logging.info('Homepage served.')
    return render_template("dance_destination.html")


@app.route('/events', methods=['GET'])
def search_event():
    """Search for event."""

    # Get from variables.
    genre = request.args.get('genre')
    location = request.args.get('location') or 'San Francisco'
    distance = request.args.get('distance') or 25
    measurement = request.args.get('measurement') or 'mi'
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
        elect_events = []

        # If genre is Electronic pull data from database where 19hz website results is saved.
        if genre == 'Electronic':
            elect_events = Event.query.all() 

        # If the response was successful use the list of events from the returned JSON
        if response.ok:
            logging.info(f'EventBrite response was successful with status_code: {response.status_code}')
            data = response.json()
            events = data['events']
            for event in events:
                if event.get('summary'):
                    event['summary'] = bleach.clean(event['summary'])

        # If there was an error (status code between 400 and 600), use an empty list
        else:
            logging.warning(f'Unable to recieve EventBrite response, status_code: {response.status_code}')
            logging.warning(f'Payload: {payload}')
            flash(f"""The eventbrite API has deprecated the /events/search \
                      endpoint, so there were no Eventbrite events found \
                      for this search.""")
            
            events = []
        

        return render_template("events.html",
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

    if user:
        flash("We Have Danced Before! Please Log In!")
        return redirect("/register")
    else:
        new_user = User(fname=fname, lname=lname, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        
        session['user_id'] = new_user.user_id

        flash(f"{new_user.fname} Welcome! Shall We Dance?")
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
        flash("We Haven't Danced Yet! Please Register.")
        return redirect('/register')

    if user.password != password:
        print(user.password)
        flash('Last Time You Used Different Password!')
        return redirect('/login')

    session['user_id'] = user.user_id

    flash(f'{user.fname} Shall We Dance Again?')
    return redirect(f'/')



@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash(f'You Are Already Missed! Please Come Back Soon!')
    return redirect('/')
  


@app.route('/about')
def about():
    """Homepage."""

    return render_template('about.html')


if __name__ == '__main__':
    # set debug=True here, to invoke the DebugToolbarExtension 
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.config['SECRET_KEY'] = "<MySecretServerKey>"

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

