"""Dance Destination."""

from jinja2 import StrictUndefined 

from flask_debugtoolbar import DebugToolbarExtension

from flask import Flask, render_template, redirect, request, flash, session

from model import User, Event, Genre, UserEvent, EventGenre, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "Something I don't want you to guess!"

#if an undefined variable used in Jinja2, raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Homepage."""

   
    return render_template("dance_destination.html")




@app.route('/', methods=['POST'])
def search_event():
    """Search for event."""

    events = Event.query.all()

    genre = request.form["genre"]
    location = request.form["location"]
    date = request.form["date"]

    for event in events:
        if (genre == events.genres and location == events.location and date == events.date):
            print(f"{events.name} {events.genres} {events.date} {events.location} {events.price} {events.image}")

        else:
            print(f"So sorry! No event found.")


    return redirect("events.html")





@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]
    

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
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("This email is not registered!")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")
def eventbrite_api_venue(venue_id):

    from urllib import request

    headers = {
      'Authorization': 'Bearer VNEIADCZTTMUDAN7533X',
      'Content-Type': 'application/json'
    }
    req = request.Request(f'https://www.eventbriteapi.com/v3/venues/{venue_id}/', headers=headers)

    response_body = request.urlopen(req).read()
    print(response_body)

    return response_body    

def eventbrite_api_request(location='San+Francisco',price='free',date=''):
    """Request data from Eventbrite API with filters requested."""

    from urllib import request

    headers = {
      'Authorization': 'Bearer VNEIADCZTTMUDAN7533X',
      'Content-Type': 'application/json'
    }
    req = request.Request(f'https://www.eventbriteapi.com/v3/events/search/?q=dance&location.address={location}&price={price}&start_date.range_start={date}', headers=headers)

    response_body = request.urlopen(req).read()
    print(response_body)

    return response_body

@app.route("/events")
def show_events():
    """Show info about event."""

    events = eventbrite_api_request() #Call Eventbrite API function in event page

    event_query = Event.query


    # check for parameters
    location = request.args.get('location')
    genre = request.args.get('genre')
    date = request.args.get('date')


    # check the users input and pass it to the API request
    if location:
        event_query = event_query.filter_by(location=location)

    if genre:
        event_query = event_query.filter_by(genres=genres)

    if date:
        event_query = event_query.filter_by(date=date)


    events = event_query.all()
    print(event_query)

    return render_template("events.html", events=events)





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