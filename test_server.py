"""Testing Flask."""

import server
import unittest

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def index(self):
        """Check index page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.get('/')

        # Compare result.data with assert method
        self.assertIn(b'<h4>What Are You in the Mood Today?</h4>', result.data)
    
    def search_event(self):
        """Test that /events route processes form data correctly."""

        client = server.app.test_client()
        result = client.post('/events', data={'genre' : 'Jazz'})

        self.assertIn(b'<h2> Events List:</h2>', result.data)


class MyAppIntegrationTestCase(unittest.TestCase):
    """Integration test: testing Flask server."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        return
        
    def register_form(self):
        result = self.client.get('/register')
        self.assertIn(b'<h1>Register</h1>', result.data)
        
    def register_process(self):
        result = self.client.post('/register', data={'fname' : 'Test',
                                                     'lname' : 'Test',
                                                     'email' : 'test@test.com',
                                                     'password' : 'testtest'})
        self.assertIn(b'<h4>What Are You in the Mood Today?</h4>', result.data)
        

    
if __name__ == '__main__':
    # If called like a script, run tests
    unittest.main()
