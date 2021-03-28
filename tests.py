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

        response = self.client.post('/search_results')
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.client.post('/add_member', data={
            'name': 'Martin',
            'contact': '9763525',
            'email': 'test@gmail.com',
            'dob': '28-10-1997'
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/add_book', data={
            'title': 'Martins Bio',
            'author': 'John',
            'isbn': '135416544',
            'publisher': 'Mc graw hill',
            'publication_date': '28-10-1997',
            'pages': '300',
            'language': 'English',
            'total_qty': '35'
        })
        self.assertEqual(response.status_code, 200)


if '__name__' == '__main__':
    unittest.main()
