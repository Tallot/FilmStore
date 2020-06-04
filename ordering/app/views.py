import db
import requests
import json
import sqlite3
import requests
import settings
import hazelcast
from aiohttp import web
from db import commit_txn, get_user_films

config = hazelcast.ClientConfig()
config.network_config.addresses.append(settings.hazelcast_ip)
hz = hazelcast.HazelcastClient(config=config)

stat_storage = hz.get_map("stat_storage")


async def index(request):
    return web.json_response({'succcess': True})


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
            resp = await requests.get(f'{settings.inventory_service_addr}/primary_title', params=payload)
            resp_json = resp.json()
            if resp_json['success']:
                for item in resp_json['films']:
                    film_id = item['id']
                    film_resp = await requests.get(f'{settings.inventory_service_addr}/id', params={'film_id': film_id})
                film_price = film_resp.json()['film']['price']
                # Request to Accounting Service
                resp  = await requests.post(f'{settings.accounting_service_addr}/buy',
                        json={'id': film_id, 'cost': film_price})
                stat_storage.lock('buy_lock')
                stat_storage.put(film_id, stat_storage.get(film_id).result() + film_price)
                stat_storage.unlock('buy_lock')
            else:
                raise Exception('Could not fetch inventory data')
        return web.json_response({'success': True})
    except sqlite3.OperationalError:
        return web.json_response({'success': False, 'reason': 'Failed to update transactions log'})


async def popular(request):
    n = request.match_info.get('n')

    max_el = 0
    local_map = {}
    stat_storage.lock('popular_lock')
    for key, value in stat_storage.entry_set().result():
        local_map[key] = value
    stat_storage.unlock('popular_lock') 
    highest = sorted(local_map, key=local_map.get, reverse=True)[:n]
    
    return web.json_response({'success': True, 'data': highest})

    
