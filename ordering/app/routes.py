import views
from aiohttp import web

urls = [
    web.get('/', views.index),
    web.get(r'/user_films/{user_id:\d+}', views.get_user_films),
    web.post(r'/buy/{user_id:\d+}', views.buy),
    web.get(r'/popular/{n:\d+}', views.popular)
]


