import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from factories.user import UserFactory
from django.contrib.auth import get_user_model

# This creates an instance of the factory used to make mock data
faker = Factory.create()


class UserTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.namespace = 'authentication'
        self.body = {
                'username': faker.first_name(),
                'email': faker.email(),
                'password': faker.password()
            }
        self.user_body = {
                'username': self.user.username,
                'email': self.user.email,
                'password': '1234abcd'
        }
        self.new_user_body = {
                'username': self.user.username,
                'email': self.user.email,
                'password': '1234abcde'
        }
        self.not_exist= {
                'username': faker.first_name(),
                'email': faker.email(),
                'password': faker.password()
            }

        self.no_email= {
                'username': faker.first_name(),
                'email': '',
                'password': faker.password()
            }
        self.no_username= {
                'username': '',
                'email': faker.email(),
                'password': faker.password()

        }
        self.email_format= {
                'username': faker.first_name(),
                'email': 'emailformat',
                'password': faker.password()
            }
        self.password_length= {
                'username': faker.first_name(),
                'email': 'emailformat',
                'password': 'pass'
            }
        self.token = 'token'

        self.create_url = reverse(self.namespace + ':register')
        self.login_url = reverse(self.namespace + ':login')

    def test_create_user_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        response2 = self.client.post(self.create_url, self.body, format='json')
        response3 = self.client.post(self.create_url, self.no_username, format='json')
        response4 = self.client.post(self.create_url, self.no_email, format='json')
        response5 = self.client.post(self.create_url, self.email_format, format='json')
        response6 = self.client.post(self.create_url, self.password_length, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response3.status_code)
        self.assertEqual(400, response4.status_code)
        self.assertEqual(400, response5.status_code)
        self.assertEqual(400, response6.status_code)

    def test_user_login(self):
        register= self.client.post(self.create_url, self.body, format='json')
        response = self.client.post(self.login_url, self.user_body, format='json')
        response2 = self.client.post(self.login_url, self.no_email, format='json')
        response3 = self.client.post(self.login_url, self.no_username, format='json')
        response4 = self.client.post(self.login_url, self.not_exist, format='json')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(json.loads(response.content).get('user').get('token'))
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response3.status_code)
        self.assertEqual(400, response4.status_code)
