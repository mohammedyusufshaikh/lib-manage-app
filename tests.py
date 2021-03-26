import unittest
from app import create_app
from app.models import db


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_basic_request(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/get_members')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/get_books')
        self.assertEqual(response.status_code, 200)

    def test_redirects(self):
        response = self.client.get('/add_book')
        self.assertEqual(response.status_code, 200)


if '__name__' == '__main__':
    unittest.main()
