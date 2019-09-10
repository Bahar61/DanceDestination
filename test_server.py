"""Testing Flask."""

import server
import unittest
from model import connect_to_db, db, User
from server import app

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def test_index(self):
        """Check index page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.get('/')

        # Compare result.data with assert method
        self.assertIn(b'Music Genre*', result.data)
    
    def test_search_event(self):
        """Test that /events route processes form data correctly."""

        client = server.app.test_client()
        result = client.get('/events', query_string={'genre' : 'Jazz',
                                            'location' : 'San Francisco',
                                            'distance' : '25',
                                            'measurement' : 'mi' }, 
                                            follow_redirects=True)

        # self.assertEqual(result.status_code, 200)
        self.assertIn(b'Events List:', result.data)

    def test_about(self):
        """Check about page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.get('/about')

        # Compare result.data with assert method
        self.assertIn(b'About', result.data)


class MyAppIntegrationTestCase(unittest.TestCase):
    """Integration test: testing Flask server."""

    def setUp(self):
        # Connect to database
        connect_to_db(server.app)

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        user =User.query.filter_by(email='ba@some.com').one()

        db.session.delete(user)

        db.session.commit()

        
    def test_register_form(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Register', result.data)
        

    def test_register_process(self):
        result = self.client.post('/register', data={'fname' : 'B',
                                                     'lname' : 'A',
                                                     'email' : 'ba@some.com',
                                                     'password' : '12345678'}, 
                                                     follow_redirects=True)
        self.assertIn(b'Welcome! Shall We Dance?', result.data)


class MyAppIntegrationTestCase(unittest.TestCase):
    """Integration test: testing Flask server."""

    def setUp(self):
        # Connect to database
        connect_to_db(server.app)

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        return

        
    def test_register_form(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Register', result.data)
        
    def test_existing_user_register_process(self):
        result = self.client.post('/register', data={'fname' : 'Test',
                                                     'lname' : 'Test',
                                                     'email' : 'test@test.com',
                                                     'password' : '12345678'}, 
                                                     follow_redirects=True)
        self.assertIn(b'We Have Danced Before! Please Log In!', result.data)
    def test_login(self):
        """Test login page."""

        result = self.client.post('/login',
                                  data={'email': 'test@test.com', 'password': '12345678'},
                                  follow_redirects=True)
        self.assertIn(b'Shall We Dance Again?', result.data)
        

    
if __name__ == '__main__':
    # If called like a script, run tests
    unittest.main()
