from model import User, Event, Genre, connect_to_db, db
from server import app
from datetime import datetime
import os

# user faker for fake data


if __name__ == '__main__':

    # Drop database and recreate it
    os.system('dropdb dance_event')
    os.system('createdb dance_event')

    connect_to_db(app)
    print('Connected to db')

    db.create_all()

    
    user1 = User(fname='Test1', lname='Test1', email='Test1', password='Test1')
    user2 = User(fname='Test2', lname='Test2', email='Test2', password='Test2')
    user3 = User(fname='Test3', lname='Test3', email='Test3', password='Test3')
    user4 = User(fname='Test4', lname='Test4', email='Test4', password='Test4')
    user5 = User(fname='Test5', lname='Test5', email='Test5', password='Test5')
    user6 = User(fname='Test6', lname='Test6', email='Test6', password='Test6')
    user7 = User(fname='Test7', lname='Test7', email='Test7', password='Test7')

    event1 = Event(date=datetime.now(),
                   location='California',
                   price=25.0,
                   name='Hip Hop Dance Time')
    event2 = Event(date=datetime.now(),
                   location='Nevada',
                   price=30.0,
                   name='Jazz Dance Time')
    event3 = Event(date=datetime.now(),
                   location='Arizona',
                   price=0.0,
                   name='Salsa Dance Time')
    event4 = Event(date=datetime.now(),
                   location='New York',
                   price=20.0,
                   name='Reggae Dance Time')
    event5 = Event(date=datetime.now(),
                   location='Oregon',
                   price=35.0,
                   name='Electronic Dance Time')
    event6 = Event(date=datetime.now(),
                   location='Florida',
                   price=25.0,
                   name='House Dance Time')
    event7 = Event(date=datetime.now(),
                   location='Texas',
                   price=20.0,
                   name='African Dance Time')

    Hip_Hop = Genre(music_genre='Hip Hop')
    Jazz = Genre(music_genre='Jazz')
    Salsa = Genre(music_genre='Salsa')
    Reggae = Genre(music_genre='Reggae')
    Electronic = Genre(music_genre='Electronic')
    House = Genre(music_genre='House')
    African = Genre(music_genre='African')

    event1.genres.append(Hip_Hop)
    event2.genres.append(Jazz)
    event3.genres.append(Salsa)
    event4.genres.append(Reggae)
    event5.genres.append(Electronic)
    event6.genres.append(House)
    event7.genres.append(African)

    user1.events.append(event1)
    user2.events.append(event2)
    user3.events.append(event3)
    user4.events.append(event4)
    user5.events.append(event5)
    user6.events.append(event6)
    user7.events.append(event7)

    db.session.add_all([user1, user2, user3, user4, user5, user6, user7, event1, event2, event3, event4, event5, event6, event7, Hip_Hop, Jazz, Salsa, Reggae, Electronic, House, African])
    db.session.commit()