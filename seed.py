"""Utility file to seed dance_event database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Event
from model import Genre
from model import UserEvent
from model import EventGenre

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


        event = Event(date=date,
                      location=location,
                      price=price)


        # add to the session to store
        db.session.add(event)

    # commit the work
    db.session.commit()



def music_genre():
    """."""

    print("Music Genre")

    genre = Genre(music_genre=music_genre)

    #add to the session to store
    db.session.add(genre)

    #commit the work
    db.session.commit()



def user_event():
    """Load user event"""
    print("User Event")

    userevent = UserEvent(user_event_id=user_event_id,
                          user_id=user_id,
                          event_id=event_id)


     #add to the session to store
    db.session.add(userevent)

    #commit the work
    db.session.commit()



def event_genre():
    """Load event genre """

    print("Event Genre")

    eventgenre = EventGenre(event_music_id=event_music_id,
                           genre_id=genre_id,
                           event_id=event_id)


    #add to the session to store
    db.session.add(eventgenre)

    #commit the work
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_events()
    music_genre()
    user_event()
    event_genre()
    set_val_event_id()
    set_val_user_id()