"""Models and database functions for Dance Event project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of event website."""

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
    name = db.Column(db.String(70), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(70), nullable=False)
    price = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(100))

    genres = db.relationship('Genre',
                             secondary='event_music',
                             backref='events')
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Event event_id={self.event_id} 
                                   date={self.date.strftime('%d-%b-%Y')} 
                                   location={self.location}
                                    price={self.price}>"""


    
class Genre(db.Model):
    """Music genre of dance event """

    __tablename__ = "genres"
    # music genre model class

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    music_genre = db.Column(db.String(70), nullable=False)
    


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Genre genre_id={self.genre_id} 
                                   music_genre={self.music_genre}>"""



class UserEvent(db.Model):
    """User events"""

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
    

class EventGenre(db.Model):
    """Event music type"""

    __tablename__ = "event_music"
    # event music type model class

    event_music_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_id = db.Column(db.Integer,
                         db.ForeignKey('genres.genre_id'))
    event_id = db.Column(db.Integer, 
                        db.ForeignKey('events.event_id'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<EventGenre event_music_id={self.event_music_id} 
                                          genre_id={self.genre_id} 
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
