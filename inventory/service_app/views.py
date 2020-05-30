import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Film


def index(request):
    return HttpResponse('Inventory Service main page')


def get_by_title(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('primary_title')
            if title == '':
                return JsonResponse({'success': False, 'error': 'empty data'})
            # NOW: case insensitive search containing requested words
            # TODO: fuzzy string search
            film_objects = Film.objects.filter(primary_title__icontains=title)
            if len(film_objects) == 0:
                return JsonResponse({'success': True, 'error': None, 'films': []})
            else:
                return JsonResponse({'success': True, 'error': None, 'films': list(film_objects.values())})
        except Exception as ex:
            return JsonResponse({'success': False, 'error': 'missing title attribute'})


def get_filtered_films(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('filters'))
            conditions = {}
            if not isinstance(data, dict):
                return JsonResponse({'success': False, 'error': 'wrong type of filters attribute'})

            all_any_flag = True  # check if none of the filters are set and abort if they are
            for key, val in data.items():
                if data[key] != 'any':
                    all_any_flag = False
                    # make appropriate request keys for django API
                    if key == 'runtime_minutes':
                        conditions[key+'__lte'] = val
                    elif key == 'average_rating':
                        conditions[key+'__gte'] = val
                    elif key == 'genres':
                        conditions[key+'__contains'] = val
                    elif key == 'directors':
                        conditions[key+'__contains'] = val
                    else:
                        conditions[key] = val

            if all_any_flag:  # do not allow obtaining all the database
                return JsonResponse({'success': False, 'error': 'at least one filter value must be set'})

            results = Film.objects.filter(**conditions)

            if len(results) == 0:
                return JsonResponse({'success': True, 'error': None, 'films': []})
            else:
                return JsonResponse({'success': True, 'error': None, 'films': list(results.values())})

        except Exception as ex:
            return JsonResponse({'success': False, 'error': 'wrong filters attribute(s)'})


def vote_for_film(request):
    if request.method == 'POST':
        try:
            film_id = request.POST.get('film_id')
            mark = request.POST.get('mark')
            mark = float(mark)
            assert 0.0 <= mark <= 10.0, 'wrong range'
            obj = Film.objects.get(title_alphanum=film_id)
            old_rate, old_votes = obj.average_rating, obj.num_votes
            new_votes = old_votes + 1
            new_rate = old_votes * old_rate / new_votes + mark/new_votes
            Film.objects.filter(title_alphanum=film_id).update(average_rating=new_rate,
                                                               num_votes=new_votes)
            return JsonResponse({'success': True, 'error': None})

        except Exception as ex:
            return JsonResponse({'success': False, 'error': 'internal error'})


def insert_film(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('new_film'))
            data_attribs = [key for key in data]
            check_attribs = ['title_alphanum', 'primary_title',
                             'is_adult', 'start_year', 'runtime_minutes',
                             'genres',
                             'directors', 'average_rating', 'num_votes']

            assert data_attribs == check_attribs, 'Bad attributes'

            new_film = Film(**data)
            new_film.save()
            return JsonResponse({'success': True, 'error': None})
        except Exception as ex:
            return JsonResponse({'success': False, 'error': 'internal error'})
