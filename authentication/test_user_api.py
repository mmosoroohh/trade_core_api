import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from factories.users import UserFactory
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
                'password': faker.password(),
                'is_holiday': faker.boolean(chance_of_getting_true=50)
            }
        self.user_body = {
                'username': self.user.username,
                'email': self.user.email,
                'password': '1234abcd',
                'is_holiday': faker.boolean(chance_of_getting_true=50) 
        }
        self.new_user_body = {
                'username': self.user.username,
                'email': self.user.email,
                'password': '1234abcde',
                'is_holiday': faker.boolean(chance_of_getting_true=50) 
        }
        self.not_exist= {
                'username': faker.first_name(),
                'email': faker.email(),
                'password': faker.password(),
                'is_holiday': faker.boolean(chance_of_getting_true=50) 
            }

        self.no_email= {
                'username': faker.first_name(),
                'email': '',
                'password': faker.password(),
                'is_holiday': faker.boolean(chance_of_getting_true=50) 
            }
        self.no_username= {
                'username': '',
                'email': faker.email(),
                'password': faker.password(),
                'is_holiday': faker.boolean(chance_of_getting_true=50) 

        }
        self.email_format= {
                'username': faker.first_name(),
                'email': 'emailformat',
                'password': faker.password(),
                'is_holiday': faker.boolean(chance_of_getting_true=50) 
            }
        self.password_length= {
                'username': faker.first_name(),
                'email': 'emailformat',
                'password': 'pass',
                'is_holiday': faker.boolean(chance_of_getting_true=50) 
            }
        self.token = 'token'

        self.create_url = reverse(self.namespace + ':register')
        self.login_url = reverse(self.namespace + ':login')
        self.retrieve_user_url = reverse(self.namespace + ':specific_user')

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
        self.assertIsNotNone(json.loads(response.content).get('token'))
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response3.status_code)
        self.assertEqual(400, response4.status_code)
        self.assertContains(response, self.user)

    def test_same_case(self):
        self.user_body.update({'username':self.user_body['username'].upper()})
        response= self.client.post(self.create_url, self.user_body, format='json')
        self.assertEqual(400, response.status_code)


    def test_retrieve_logged_in_user(self):
        response = self.client.get(self.retrieve_user_url)
        self.assertEqual(200, response.status_code)