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
        # test exceptions

        self.assertEqual(len(result1['films']), 1)
        self.assertEqual(result1['films'][0]['primary_title'], 'test_film1')
        self.assertEqual(len(result2['films']), 2)

    def test_get_filtered_films_view(self):
        # test filtering functionality
        response1 = self.client.post('/service_app/filter/',
                                     {'filters': json.dumps({'is_adult': 'any',
                                                             'start_year': 'any',
                                                             'runtime_minutes': 'any',
                                                             'genres': 'test_genre2',
                                                             'average_rating': 'any'})})
        result1 = json.loads(response1.content.decode('utf-8'))
        self.assertEqual(len(result1['films']), 2)

        response2 = self.client.post('/service_app/filter/',
                                     {'filters': json.dumps({'is_adult': 'any',
                                                             'start_year': 'any',
                                                             'runtime_minutes': 'any',
                                                             'genres': 'any',
                                                             'average_rating': 'any'})})
        result2 = json.loads(response2.content.decode('utf-8'))
        self.assertEqual(result2['error'], 'at least one filter value must be set')

    def test_vote_for_film_view(self):
        response = self.client.post('/service_app/vote/',
                                    {'film_id': 12, 'mark': 9.9})
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result['success'], True)
        self.assertEqual(Film.objects.get(
            pk=12).average_rating, 8.804803493449782)

        response2 = self.client.post('/service_app/vote/',
                                     {'film_id': 13, 'mark': 12.9})
        result2 = json.loads(response2.content.decode('utf-8'))
        self.assertEqual(result2['success'], False)

    def test_insert_film_view(self):
        correct_dict = {'title_alphanum': 'tt9999999',
                        'primary_title': 'test_title999999',
                        'is_adult': True,
                        'start_year': 1289,
                        'runtime_minutes': 13,
                        'genres': ['gg'],
                        'directors': ['wp', 'gl', 'hf'],
                        'average_rating': 6.7,
                        'num_votes': 1488}
        incorrect_dict = {'title_alphanum': 'tt6666666',
                          'primary_title': 'test_title666666',
                          'is_adult': True,
                          'start_year': 1289,
                          'runtime_minutes': 13,
                          'genres': ['gg'],
                          'dictors': ['wp', 'gl', 'hf'],
                          'average_rating': 6.7}

        response = self.client.post('/service_app/insert/',
                                    {'new_film': json.dumps(correct_dict)})
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result['success'], True)

        response2 = self.client.post('/service_app/insert/',
                                     {'new_film': json.dumps(incorrect_dict)})
        result2 = json.loads(response2.content.decode('utf-8'))
        self.assertEqual(result2['success'], False)

    def test_enum_ids_view(self):
        response = self.client.get('/service_app/enum/')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result['success'], True)

    def test_get_by_id_view(self):
        response = self.client.get('/service_app/id/',
                                   {'film_id': 1})
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result['success'], True)
