from django.test import TestCase
from django.core import serializers
from faker import Faker
import random
import json
from datetime import (
    datetime,
    timedelta
)
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
        print('setUpClass')

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
                Screening.objects.create(**cls._fake_screening_data(
                    cinema=cinema,
                    movie=random.choice(Movie.objects.all())
                    )
                )

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
    def _fake_screening_data(cls, cinema, movie):
        return dict(
            cinema=cinema,
            movie=movie,
            screening_room=random.randint(1, 34),
            date=datetime(
                random.randint(2018, 2019),
                random.randint(1, 12),
                random.randint(1, 28),
                random.randint(0, 23),
                random.randint(0, 59)
                )
            )

    def test_a_list_cinemas(self):
        response = self.client.get('/cinemas/', {}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_b_cinema_details(self):
        response = self.client.get('/cinemas/1/', {}, format='json')
        self.assertEqual(response.status_code, 200)

    def test3_add_cinema(self):
        new_cinema_data = self._fake_cinema_data()
        response = self.client.post('/cinemas/', new_cinema_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cinema.objects.filter(**new_cinema_data).count(), 1)

    def test_c_update_cinema(self):
        updated_cinema_data = self._fake_cinema_data()
        response = self.client.patch('/cinemas/1/', updated_cinema_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.filter(**updated_cinema_data).count(), 1)

    def test_d_update_non_existing_cinema(self):
        updated_cinema_data = self._fake_cinema_data()
        response = self.client.patch('/cinemas/9999999999999999999999999999/', updated_cinema_data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_e_delete_cinema(self):
        response = self.client.delete('/cinemas/1/', {}, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Cinema.objects.filter(pk=1).count(), 0)

    def test_f_delete_non_existing_cinema(self):
        response = self.client.delete('/cinemas/9999999999999999999999999999/', {}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_g_list_screenings(self):
        response = self.client.get('/screenings/', {}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_h_screening_details(self):
        response = self.client.get('/screenings/1/', {}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_i_add_screening(self):
        new_screening_data = self._fake_screening_data(
            cinema=random.choice(Cinema.objects.all()),
            movie=random.choice(Movie.objects.all())
        )
        new_screening_json_data = dict(new_screening_data)
        new_screening_json_data.update(
            {
                'cinema': new_screening_data['cinema'].name,
                'movie': new_screening_data['movie'].title
            }
        )
        response = self.client.post('/screenings/', new_screening_json_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Screening.objects.filter(**new_screening_data).count(), 1)

    def test_j_update_screening(self):
        updated_screening_data = self._fake_screening_data(
            cinema=random.choice(Cinema.objects.all()),
            movie=random.choice(Movie.objects.all())
        )
        updated_screening_json_data = dict(updated_screening_data)
        updated_screening_json_data.update(
            {
                'cinema': updated_screening_data['cinema'].name,
                'movie': updated_screening_data['movie'].title
            }
        )
        response = self.client.patch('/screenings/1/', updated_screening_json_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Screening.objects.filter(**updated_screening_data).count(), 1)

    def test_k_update_non_existing_screening(self):
        updated_screening_data = self._fake_screening_data(
            cinema=random.choice(Cinema.objects.all()),
            movie=random.choice(Movie.objects.all())
        )
        updated_screening_json_data = dict(updated_screening_data)
        updated_screening_json_data.update(
            {
                'cinema': updated_screening_data['cinema'].name,
                'movie': updated_screening_data['movie'].title
            }
        )
        response = self.client.patch('/screenings/9999999999999999999999999999/', updated_screening_json_data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_l_delete_screening(self):
        response = self.client.delete('/screenings/1/', {}, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Screening.objects.filter(pk=1).count(), 0)

    def test_m_delete_non_existing_screening(self):
        response = self.client.delete('/screenings/9999999999999999999999999999/', {}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_n_get_cinemas_with_movies_played_in_nearest_30_days_when_such_a_movies_exist(self):
        cinema = Cinema.objects.filter(pk=2).first()
        movie = Movie.objects.filter(pk=2).first()
        Screening.objects.create(
            cinema=cinema,
            movie=movie,
            date=datetime.now() + timedelta(15)
        )
        response = self.client.get('/cinemas_current_movies/2/', {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(movie.title, json.loads(response.content)['movies'])

    def test_o_get_cinemas_with_movies_played_in_nearest_30_days_when_such_a_movies_does_not_exist(self):
        start_day = datetime.now()
        end_day = start_day + timedelta(30)
        Movie.objects.filter(
            screening__date__gte=start_day,
            screening__date__lt=end_day
        ).delete()
        response = self.client.get('/cinemas_current_movies/2/', {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['movies'], [])

    def test_p_get_screenings_of_given_existing_cinema(self):
        cinema = Cinema.objects.all().first()
        screenings = Screening.objects.filter(cinema__name=cinema.name)
        response = self.client.get(
            '/screenings/',
            {
                'cinema__name': cinema.name,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        for screening_obj in json.loads(serializers.serialize('json', screenings)):
            screening_obj_cleaned = screening_obj['fields']
            screening_obj_cleaned.update(
                {
                    'id': screening_obj['pk'],
                    'cinema': Cinema.objects.get(pk=screening_obj_cleaned['cinema']).name,
                    'movie': Movie.objects.get(pk=screening_obj_cleaned['movie']).title
                }
            )
            self.assertIn(json.loads(json.dumps(screening_obj_cleaned)), json.loads(response.content))

    def test_q_get_screenings_of_given_non_existing_cinema(self):
        response = self.client.get(
            '/screenings/',
            {
                'cinema__name': '....non-existing-cinema-name_jisbhb!!@@##$$',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_r_get_screenings_of_given_existing_movie(self):
        movie = Movie.objects.all().first()
        screenings = Screening.objects.filter(movie__title=movie.title)
        response = self.client.get(
            '/screenings/',
            {
                'movie__title': movie.title,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        for screening_obj in json.loads(serializers.serialize('json', screenings)):
            screening_obj_cleaned = screening_obj['fields']
            screening_obj_cleaned.update(
                {
                    'id': screening_obj['pk'],
                    'cinema': Cinema.objects.get(pk=screening_obj_cleaned['cinema']).name,
                    'movie': Movie.objects.get(pk=screening_obj_cleaned['movie']).title
                }
            )
            self.assertIn(json.loads(json.dumps(screening_obj_cleaned)), json.loads(response.content))

    def test_s_get_screenings_of_given_non_existing_movie(self):
        response = self.client.get(
            '/screenings/',
            {
                'movie__title': '....non-existing-movie-title_oiwnvnwevnw889!!@@##$$',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_t_get_screenings_of_given_existing_cinema_and_movie(self):
        cinema = Cinema.objects.all().first()
        movie = Movie.objects.all().first()
        new_screening_data = self._fake_screening_data(cinema, movie)
        screening = Screening.objects.create(**new_screening_data)
        response = self.client.get(
            '/screenings/',
            {
                'cinema__name': screening.cinema.name,
                'movie__title': screening.movie.title,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        new_screening_json_data = dict(new_screening_data)
        new_screening_json_data.update(
            {
                'id': screening.id,
                'cinema': cinema.name,
                'movie': movie.title,
                'screening_room': str(screening.screening_room),
                'date': new_screening_data['date'].isoformat() + 'Z'
            }
        )
        self.assertIn(json.loads(json.dumps(new_screening_json_data)), json.loads(response.content))

    def test_u_get_screenings_of_given_existing_cinema_and_non_existing_movie(self):
        cinema = Cinema.objects.all().first()
        response = self.client.get(
            '/screenings/',
            {
                'cinema__name': cinema.name,
                'movie__title': '....non-existing-movie-title_oiwnvnwevnw889!!@@##$$',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_u_get_screenings_of_given_existing_movie_and_non_existing_cinema(self):
        movie = Movie.objects.all().first()
        response = self.client.get(
            '/screenings/',
            {
                'cinema__name': '....non-existing-cinema-name_oiwnvnwevnw889!!@@##$$',
                'movie__title': movie.title,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')
