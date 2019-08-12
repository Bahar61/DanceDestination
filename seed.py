"""Utility file to seed dance_event database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import DanceEvent
from model import MusicGenre
from model import UserEvent
from model import EventMusicGenre

from model import connect_to_db, db
from server import app
from datetime import datetime



def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/user_data"):
        row = row.rstrip()
        user_id, fname, lname, email, password = row.split("|")

        user = User(user_id=user_id,
                    fname=fname, 
                    lname=lname,
                    email=email,
                    password=password)

        # add to the session
        db.session.add(user)

    #commit the work
    db.session.commit()



def load_events():
    """Load events from event_data into database."""

    print("Events")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate movies
    Event.query.delete()

    # Read event_data file and insert data
    for row in open("seed_data/event_data"):
        row = row.rstrip()
        event_id, date, location, price = row.split("|")

        #convert string time to Datetime
        if date:
            date = datetime.strptime(date, "%d-%b-%Y")
        else:
            date = None


        event = Event(event_id=event_id,
                      date=date,
                      location=location,
                      price=price)


        # add to the session to store
        db.session.add(event)

    # commit the work
    db.session.commit()



def music_genre():
    """."""

    print("Music Genre")

    

        #add to the session to store
        db.session.add(rating)

    #commit the work
    db.session.commit()


def set_val_event_id():
    """Set value for the next event_id after seeding database"""

    # Get the Max event_id in the database
    result = db.session.query(func.max(Event.event_id)).one()
    max_id = int(result[0])

    # Set the value for the next event_id to be max_id + 1
    query = "SELECT setval('event_event_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
