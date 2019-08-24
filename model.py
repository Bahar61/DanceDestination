"""Models and database functions for DanceDestination project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"
    # user model class

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(70), nullable=False)
    lname = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(70), nullable=False)

    events = db.relationship('Event',
                             secondary='users_event',
                             backref='users')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User user_id={self.user_id} 
                            fname={self.fname} 
                            lname={self.lname}
                            email={self.email} 
                            password={self.password}>"""



class Event(db.Model):
    """Event of website."""

    __tablename__ = "events"
    # event model class

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(300), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    organizer = db.Column(db.String(100), nullable=True)
    link = db.Column(db.String(300), nullable=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<event_id={self.event_id}
                    name={self.name}
                    date={self.date}
                    location={self.location}
                    price={self.price}
                    genre={self.genre}
                    age={self.age}
                    organizer={self.organizer}
                    link={self.link}>"""


    
class UserEvent(db.Model):
    """User events."""

    __tablename__ = "users_event"
    # users event model class

    user_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.event_id'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<UserEvent user_event_id={self.user_event_id} 
                   user_id={self.user_id}
                   event_id={self.event_id}>"""
    


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dance_event'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)




if __name__ == "__main__":
    # When we run this module interactively, we are able to work with the database directly.

    from server import app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")
