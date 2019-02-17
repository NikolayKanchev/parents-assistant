import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Faker('email')
    password = factory.Faker('password')


class ChildFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Child

    date_of_birth = factory.Faker(
        'date_of_birth', minimum_age=0, maximum_age=15
    )
    user = factory.SubFactory(UserFactory)
