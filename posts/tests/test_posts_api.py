from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from ...factories import PostFactory, UserFactory

faker = Factory.create()


class PostApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.namespace = 'post_api'
        self.body = {
            'title': faker.name(),
            'description': faker.text(),
            'body': faker.text()
        }
        self.create_url = reverse(self.namespace + ':create')
        self.list_url = reverse(self.namespace + ':list')
        self.update_url = reverse(
            self.namespace + ':update', kwargs={'slug': self.post.id})
        self.delete_url = reverse(
            self.namespace + ':delete', kwargs={'slug': self.post.id})
        self.retrieve_url = reverse(
            self.namespace + ':detail', kwargs={'slug': self.post.id})
        

    def test_create_post_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.assertEqual(201, response.status_code)

    def test_retrieve_post_api(self):
        response = self.client.get(self.retrieve_url)
        self.assertContains(response, self.post)

    def test_listing_posts_api(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, self.posts)

    def test_update_posts_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.update_url = reverse(
            self.namespace + ':update', kwargs={'pk': response.data.get('pk')})
        response = self.client.put(self.update_url, self.body)
        self.assertEqual(200, response.status_code)

    def test_delete_post_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.delete_url = reverse(
            self.namespace + ':delete', kwargs={'pk': response.data.get('pk')})
        response = self.client.delete(self.delete_url)
        self.assertEqual(204, response.status_code)
