from django.urls import path
from . import views

app_name = 'service_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('title/', views.get_by_title, name='title'),
    path('filter/', views.get_filtered_films, name='filter'),
    path('vote/', views.vote_for_film,  name='vote'),
    path('insert/', views.insert_film, name='insert'),
    path('enum/', views._enum_ids, name='enum'),
    path('id/', views._get_by_id, name='id'),
]
