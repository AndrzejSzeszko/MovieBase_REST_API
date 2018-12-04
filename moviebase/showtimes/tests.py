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
    fake = Faker('pl-PL')
    
    @classmethod
    def setUpClass(cls):

        for _ in range(4):
            Person.objects.create(**cls._fake_person_data())

        cls.available_people = Person.objects.all()
        for _ in range(3):
            new_movie = Movie.objects.create(**cls._fake_movie_data())
            new_movie.actors.set(random.sample([person for person in cls.available_people], 3))

        for _ in range(3):
            Cinema.objects.create(**cls._fake_cinema_data())

        for cinema in Cinema.objects.all():
            for _ in range(5):
                Screening.objects.create(**cls._fake_screening_data(cinema))

    @classmethod
    def _fake_person_data(cls):
        return dict(
            name=cls.fake.name()
        )

    @classmethod
    def _fake_movie_data(cls):
        return dict(
            title=cls.fake.text(20)[:-1],
            description=cls.fake.text(100),
            director=random.choice(cls.available_people),
            year=random.randint(1900, 2019),
        )

    @classmethod
    def _fake_cinema_data(cls):
        return dict(
           name=cls.fake.company(),
           city=cls.fake.city()
        )

    @classmethod
    def _fake_screening_data(cls, cinema):
        return dict(
            cinema=cinema,
            movie=random.choice(Movie.objects.all()),
            date=datetime(
                random.randint(2018, 2019),
                random.randint(1, 12),
                random.randint(1, 28),
                random.randint(0, 23),
                random.randint(0, 59)
                )
            )

    def test_add_cinema(self):
        new_cinema_data = self._fake_cinema_data()
        response = self.client.post('')

    @classmethod
    def tearDownClass(cls):
        pass
