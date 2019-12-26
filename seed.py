"""Utility file to seed dance_event database from 19hz data in seed_data/"""

from sqlalchemy import func
from model import User, Event, UserEvent
from model import connect_to_db, db
from server import app
from data_base_config import BASE_PATH
import logging


# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
f_handler = logging.FileHandler('seed.log')
logger.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)


# Add handlers to the logger
logger.addHandler(f_handler)


def create_users():
    """Create users and insert into database."""
    print('Users')


    # Test user for testing
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
    logger.info('Users table updated successfully.')
    
def load_events():
    """Load events from csv file into database."""

    print('Events')

    # Read data from 19hz wbsite and insert data to database
    for row in open(BASE_PATH +'seed_data/19hz_scrape.csv'):
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
    logger.info('Events table updated successfully.')


def user_event():
    """Load user event"""
    print('User Event')

    
    user_id = int(user_id) 
    event_id = int(event_id) 

    userevent = UserEvent(user_id=user_id,
                          event_id=event_id,
                          )


     #add to the session to store
    db.session.add(userevent)

    #commit the work
    db.session.commit()

def update_events_database():
    # updates Events table with new data

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    logger.info('Attempting to update Events table.')
    # Import different types of data
    load_events()
    

if __name__ == '__main__':
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    create_users()
    load_events()
    # user_event()

   