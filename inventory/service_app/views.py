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
    pass


def vote_for_film(request):
    pass
