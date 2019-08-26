"""Utility file to seed dance_event database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Event, UserEvent
from model import connect_to_db, db
from server import app

def load_users():
    """Load users from u.user into database."""
    print("Users")


    # Read u.user file and insert data
    fname, lname, email, password = ('Test', 'Test', 'test@test.com', '12345678')

    user = User(fname=fname, 
                lname=lname,
                email=email,
                password=password,
                )

    # add to the session
    db.session.add(user)

    # commit the work
    db.session.commit()


def load_events():
    """Load events from event_data into database."""

    print("Events")

    # Read event_data file and insert data
    for row in open("seed_data/19hz_scrape.csv"):
        row = row.rstrip()
        name, location, date, genre, price_age, organizer, link = row.split('\t')
        
        event = Event(
            name=name,
            location=location,
            date=date,
            genre=genre,
            price_age=price_age,
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

    
    user_id = int(user_id) 
    event_id = int(event_id) 

    userevent = UserEvent(user_id=user_id,
                          event_id=event_id,
                          )


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
    # user_event()

   