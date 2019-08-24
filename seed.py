"""Utility file to seed dance_event database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Event, UserEvent
from model import connect_to_db, db
from server import app
import 19hz


def load_users():
    """Load users from u.user into database."""
    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
   
        user_id, fname, lname, email, password = row.split("|")

        user = User(user_id=user_id,
                    fname=fname, 
                    lname=lname,
                    email=email,
                    password=password)

        # add to the session
        db.session.add(user)

    # commit the work
    db.session.commit()


def load_events():
    """Load events from event_data into database."""

    print("Events")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate movies
    Event.query.delete()

    # Read event_data file and insert data
    open("seed_data/19hz.py")
        
        event = Event(
            event_id=event_id,
            name=name,
            date=date,
            location=location,
            price=price,
            genre=genre,
            age=age,
            organizer=organizer,
            link=link,
            )

        # add to the session to store
        db.session.add(event)

    # commit the work
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



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_events()
    user_event()

   