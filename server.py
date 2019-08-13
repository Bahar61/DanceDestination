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

    # Use jinja to show events in the first page
    # for loop through all events(query.all()) in jinja
    return render_template("dance-destination.html")



@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register-form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added.")
    return redirect(f"/users/{new_user.user_id}")


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



@app.route("/events/<music_genre>")
def show_event(music_genre):
    """Show info about event.
    Also, provide a button to share and add."""


    """If user is logged in let them add event."""    
    # event = Event.query(music_genre)
    # user_id = session.get("user_id")

    # if user_id:
    #     user_event_id = UserEvent.query.filter_by(
    #         user_id=user_id, event_id=event_id).first()
    # else:
    #     user_event_id = None




    return render_template("events.html", name=name,
                                          date=date,
                                          location=location,
                                          price=price,
                                          image=image)


@app.route('/About')
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
    app.config['SECRET_KEY'] = "<Something you can't guess!>"

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')