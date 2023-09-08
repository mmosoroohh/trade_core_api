from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.apps import apps
from factories.posts import PostFactory


from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.data = {
            'title': 'this is a title',
        }

    def test_model_can_create_post(self):
        post = PostFactory(title=self.data.get('title'))
        saved_post = Post.objects.get(title=self.data.get('title'))
        self.assertEqual(post, saved_post)
