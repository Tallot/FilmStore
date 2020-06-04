import db
import requests
import json
import sqlite3
import requests
import settings
import hazelcast
from aiohttp import web
from db import commit_txn, get_user_films
from django.http import HttpResponse, JsonResponse

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


def buy(request):
    try:
        user_id = request.match_info.get('user_id')
        data = request.json()
        prod_id = data['items']
        resp = requests.get(f'{settings.accounting_service_addr}/buy', json={'id': user_id, 'cost': 100})
        if not resp.json['success']:
            return JsonResponse({'success': False})
        else:
            commit_txn([prod_id], user_id, 100)
            return JsonResponse({'succcess': True})

        # for item in prod_titles:
            # # Request to Inventory Service
            # payload = {'primary_title': item}
            # resp = await requests.get(f'{settings.inventory_service_addr}/primary_title', params=payload, timeout=60.0)
            # resp_json = resp.json()
            # if resp_json['success']:
                # for item in resp_json['films']['id']
                    # film_id = item['id']
                    # film_resp = await requests.get(f'{settings.inventory_service_addr}/id', params={'film_id': film_id})
                # film_price = film_resp.json()['film']['price']
                # # Request to Accounting Service
                # resp  = await requests.post(f'{settings.accounting_service_addr}/buy',
                        # json={'id': film_id, 'cost': film_price})
                # stat_storage.lock('buy_lock')
                # stat_storage.put(film_id, stat_storage.get(film_id).result() + film_price)
                # stat_storage.unlock('buy_lock')
            # else:
                # return web.json({'success': False, 'reason': 'Failed to fetch inventory data'})
        # return web.json_response({'success': True})
    except sqlite3.OperationalError:
        return web.json_response({'success': False, 'reason': 'Failed to update transactions log'})
    except Exception as err:
        return web.json_response({'success': False, 'reason': str(err)})


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