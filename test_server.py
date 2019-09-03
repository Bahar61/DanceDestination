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


class MyAppIntegrationTestCase(unittest.TestCase):
    """Integration test: testing Flask server."""

    def setUp(self):
        # Connect to database
        connect_to_db(server.app)

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        User.query.filter_by(email='ba@some.com').delete()
        
        return
        
    def test_register_form(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Register</h1>', result.data)
        
    def test_existing_user_register_process(self):
        result = self.client.post('/register', data={'fname' : 'Test',
                                                     'lname' : 'Test',
                                                     'email' : 'test@test.com',
                                                     'password' : '12345678'}, 
                                                     follow_redirects=True)
        self.assertIn(b'We have danced before! Please Log In!', result.data)

    def test_register_process(self):
        result = self.client.post('/register', data={'fname' : 'B',
                                                     'lname' : 'A',
                                                     'email' : 'ba@some.com',
                                                     'password' : '12345678'}, 
                                                     follow_redirects=True)
        self.assertIn(b'Welcome! Shall we dance?', result.data)


    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "test@test.com", "password": "12345678"},
                                  follow_redirects=True)
        self.assertIn(b"shall we dance again?", result.data)
        

    
if __name__ == '__main__':
    # If called like a script, run tests
    unittest.main()
