import db
import aiosqlite
import requests
import json
import sqlite3
import requests
import settings
import hazelcast
from aiohttp import web
from db import commit_txn, get_user_films


async def index(request):
    return web.json_response({'succcess': 'ok'})


async def get_user_films(request):
    try:
        user_id = request.match_info.get('user_id')
        user_films = db.get_user_films(user_id)
        return web.json_response({'success': True, 'user_films': user_films})
    except:
        return web.json_response({'success': False})


async def buy(request):
    try:
        user_id = request.match_info.get('user_id')
        data = await request.json()
        prod_titles = data['items']
        for item in prod_titles:
            # Request to Inventory Service
            payload = {'primary_title': item}
            resp = requests.get(f'{settings.inventory_service_addr}/primary_title', params=payload)
            resp_json = resp.json()
            if resp_json['success']:
                # Request to Accounting Service
                # --account.cash
                # ++user.film
                # Request to Inventory
                # --film
                stat_storage.lock()
                for film in resp['films']:
                    value = stat_storage.get(film['id'])
                    # Default value = 100. need to get it from api
                    stat_storage.put(film['id'], value + 100)
                stat_storage.unlock()
            else:
                raise Exception('Could not fetch inventory data')
        return web.json_response({'success': True})
    except sqlite3.OperationalError:
        return web.json_response({'success': False, 'reason': 'Failed to update transactions log'})


async def popular(request):
    n = request.match_info.get('n')

    popular = []
    max_el = 0
    stat_storage.lock()
    local_map = stat_storage.get_map()
    highest = dict(sorted(A.iteritems(), key=operator.itemgetter(1), reverse=True)[:n])
    stat_storage.unlock()

    return web.json_response({'success': True, 'data': highest})

    
