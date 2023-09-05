import factory
from faker import Factory
from django.apps import apps
from factories.users import UserFactory

from posts.models import Post
faker = Factory.create()


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'map-title%d' % n)
    description = faker.text()
    body = faker.text()
