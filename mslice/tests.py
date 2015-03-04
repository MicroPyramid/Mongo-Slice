"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase
from django.test import Client
import pymongo

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class Test_Mongo(TestCase):

	def setUp(self):
		self.client = Client()
		self.mongoclient = pymongo.MongoClient()
		self.db = self.mongoclient.slice
		self.db.add_user('root', 'root', roles=['root'])
		self.db.post.insert({'auther': 'ravi', 'title': 'Pymongo tut','description': 'desc'})



	def test_mongo_db(self):
		self.response = self.client.get('/')
		self.assertEqual(self.response.status_code, 200)

		self.response = self.client.post('/',{})
		self.assertTrue('false' in self.response.content)
		self.assertEqual(self.response.status_code, 200)

		self.response = self.client.post('/', {'host': self.mongoclient.host, 'port': self.mongoclient.port, 'db' : 'slice', 'uid': 'root', 'pwd': 'root'})
		
		self.assertTrue('true' in self.response.content)
		self.assertEqual(self.response.status_code, 200)

		self.response = self.client.get('/info/post/')
		self.assertTrue('Pymongo tut' in self.response.content)
		self.assertEqual(self.response.status_code, 200)

