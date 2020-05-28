from django.urls import path
from . import views

app_name = 'service_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('title/', views.get_by_title, name='title'),
]
