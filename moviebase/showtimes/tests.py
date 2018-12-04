from django.test import TestCase
from faker import Faker
import random
from datetime import datetime
from rest_framework.test import APITestCase
from .models import (
    Cinema,
    Screening,
)
from movielist.models import (
    Movie,
    Person
)


class ShowtimesTestCase(APITestCase):

    def setUp(self):
        fake = Faker('pl-PL')

        for _ in range(4):
            Person.objects.create(name=fake.name())

        available_people = Person.objects.all()
        for _ in range(3):
            new_movie = Movie.objects.create(
                title=fake.text(20)[:-1],
                description=fake.text(100),
                director=random.choice(available_people),
                year=random.randint(1900, 2019),
            )
            new_movie.actors.set(random.sample(available_people, 3))

        for _ in range(3):
            Cinema.objects.create(
                name=fake.company(),
                city=fake.city()
            )

        for cinema in Cinema.objects.all():
            for _ in range(5):
                Screening.objects.create(
                    cinema=cinema,
                    movie=random.choice(Movie.objects.all()),
                    date=datetime(
                        random.randint(2018, 2019),
                        random.randint(1, 12),
                        random.randint(0, 23),
                        random.randint(0, 59)
                    )
                )


    def test_add_cinema(self):
        pass

    def tearDown(self):
        pass
