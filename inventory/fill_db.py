import json
import django
django.setup()
from service_app.models import Film


with open('fixtures/mongo_init_data.json') as data_file:
    json_data = json.loads(data_file.read())
    for film_data in json_data:
        film = Film(**film_data)
        film.save()
