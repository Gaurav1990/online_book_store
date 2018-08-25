import json

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from books.models import *


class BooksTestCase(TestCase):


    def setUp(self):
        """
        This test case is for set up some generated models values for testing purpose.
        """
        self.user = User.objects.create_user(
            'gauravnagpal2002@gmail.com',
            'gauravnagpal2002@gmail.com',
            'test'
        )
        self.client = Client()
        self.headers = {'HTTP_AUTHORIZATION': self.token_return()}
        self.dummy_data = {
            "isbn": "2323232323",
            "description": "test",
            "author_name": "Gaurav",
            "price": 799,
            "signed": True,
            "type": "romantic",
            "name": "testing"
        }

    #################################################################################

    def token_return(self):
        """
        Token which we need to send in the authorization header
        :return:
        """
        response_data = self.client.post('/login/', data=json.dumps(
            {"username": "gauravnagpal2002@gmail.com", "password": "test"}),
                                         content_type='application/json')
        response_json = json.loads(response_data.content)
        return response_json['token']

    def test_01_calling_for_authentication(self):
        """
        testcase for the /login/ url
        """
        response_data = self.client.post('/login/', data=json.dumps({"username": "gauravnagpal2002@gmail.com", "password": "test"}),
                                content_type='application/json')
        response_json = json.loads(response_data.content)
        req_keys = ["token", 'message']
        self.assertEquals(sorted(req_keys), sorted(response_json.keys()))
        self.assertEquals(response_json["message"], "User is logged in")

    def test_02_post_book(self):
        """
        Testcase for POST /book/ url

        """
        response_data = self.client.post('/book/', data=json.dumps(self.dummy_data),
                                         content_type='application/json', **self.headers)
        response_json = json.loads(response_data.content)
        req_keys = ['msg', 'book_id']
        self.assertEquals(sorted(req_keys), sorted(response_json.keys()))
        self.assertEquals(response_json["msg"], "New book entered successfully.")


    def test_03_fetch_all_books(self):
        """
        Testcase for fetching all books. GET /books/
        :return:
        """
        self.client.post('/book/', data=json.dumps(self.dummy_data),
                                         content_type='application/json', **self.headers)
        response_data = self.client.get('/books/', **self.headers)
        response_json = json.loads(response_data.content)
        req_keys = ['name', 'type', 'isbn', 'description', 'author_name', 'signed', 'price']
        self.assertEquals(1, len(response_json['Book']))

    def test_04_fetch_single_book(self):
        """
        Testcase for fetching single book GET /book/<isbn_id>/
        """
        self.client.post('/book/', data=json.dumps(self.dummy_data),
                         content_type='application/json', **self.headers)
        response_data = self.client.get('/book/2323232323/', **self.headers)
        response_json = json.loads(response_data.content)
        resp_keys = [x.encode('UTF8') for x in response_json.keys()]
        req_keys = ['name', 'id', 'type', 'isbn', 'description', 'release_date','author_name', 'signed', 'price']
        self.assertEquals(sorted(req_keys), sorted(resp_keys))

    def test_05_update_book_info(self):
        """
        Testcase for updating the book information: PUT /book/<isbn_id>/
        """
        self.client.post('/book/', data=json.dumps(self.dummy_data),
                         content_type='application/json', **self.headers)
        response_data = self.client.put('/book/2323232323/', data = json.dumps({"price": 400}),
                                        content_type='application/json', **self.headers)
        response_json = json.loads(response_data.content)
        req_keys = ['msg', 'book_id']
        self.assertEquals(sorted(req_keys), sorted(response_json.keys()))
        self.assertEquals(response_json["msg"], "Update record successfully.")

    def test_06_delete_book(self):
        """
        Testcase for deleting book record
        """
        self.client.post('/book/', data=json.dumps(self.dummy_data),
                         content_type='application/json', **self.headers)
        response_data = self.client.delete('/book/2323232323/',
                                        content_type='application/json', **self.headers)
        response_json = json.loads(response_data.content)
        req_keys = ['msg', 'book_id']
        self.assertEquals(sorted(req_keys), sorted(response_json.keys()))
        self.assertEquals(str(response_json["msg"]), "Book record deleted successfully.")
