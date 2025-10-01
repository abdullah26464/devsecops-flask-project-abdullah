import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        # Replace '/protected_route' with an actual protected route from your app
        response = self.client.get('/protected_route')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
