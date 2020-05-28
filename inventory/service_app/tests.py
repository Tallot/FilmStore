import json
from django.test import TestCase, Client

from .models import Film


class FilmTestCase(TestCase):
    def setUp(self):
        Film.objects.create(
            title_alphanum='tt0020001',
            primary_title='test_film1',
            is_adult=True,
            start_year=2020,
            runtime_minutes=127,
            genres=["test_genre1", "test_genre2"],
            directors=['test_director1'],
            average_rating=8.8,
            num_votes=228)
        Film.objects.create(
            title_alphanum='tt0020002',
            primary_title='test_film2',
            is_adult=False,
            start_year=2030,
            runtime_minutes=88,
            genres=["test_genre3", "test_genre2"],
            directors=['test_director2', 'test_director3'],
            average_rating=10.0,
            num_votes=1337)

        self.client = Client()

    def test_get_by_title_view(self):
        # test case insensitive query by title of the film
        response1 = self.client.post('/service_app/title/',
                                     {'primary_title': 'Test_Film1'})
        result1 = json.loads(response1.content.decode('utf-8'))
        response2 = self.client.post('/service_app/title/',
                                     {'primary_title': 'tEst_FilM'})
        result2 = json.loads(response2.content.decode('utf-8'))

        self.assertEqual(len(result1['films']), 1)
        self.assertEqual(result1['films'][0]['primary_title'], 'test_film1')
        self.assertEqual(len(result2['films']), 2)
