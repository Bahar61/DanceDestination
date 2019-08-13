"""Dance Destination."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import Flask, render_template, redirect, request, flash, session

from model import User, Event, Genre, UserEvent, EventGenre, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "Something you can't guess!"

#if an undefined variable used in Jinja2, raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("dance-destination.html")



@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user.html", users=users)



@app.route("/register", methods=["GET"])
def register_form():
    """Show registration form."""

    return render_template("register-form.html")



@app.route("/register", methods=["POST"])
def register_process():
    """Handle processing the registration form."""

    registration_email = request.form['email']
    registration_pass = request.form['password']

    user = User.query.filter_by(email=registration_email).first()
    
    if user:
        flash("There is an account associated with this email address! Please Login!")
    else:
        new_user = User(email=registration_email, password=registration_pass)

        db.session.add(new_user)
        db.session.commit()



    return redirect("/")



@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    user = usres.get_by_email(email)

    if not user:
        flash("The email address doesn't exist.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    session["logged_in_customer_email"] = user.email
    flash("Logged in.")
    return redirect("/")


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_customer_email"]
    flash("Logged out.")
    return redirect("/")



@app.route("/events")
def events_list():
    """Show list of events."""

    events = Event.query.all()
    return render_template("events.html", events=events)



@app.route("/events/<event_id>")
def show_event(event_id):
    """Return page showing the details of a given event.

    Show all info about a event. Also, provide a button to add that event.
    """

    event = events.get_by_id(event_id)
    print(event)
    return render_template("event-details.html",
                           display_event=event)






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')