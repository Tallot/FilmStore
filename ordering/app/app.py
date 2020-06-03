import routes
import settings
import hazelcast
from aiohttp import web
from init_db import init_connection

app = web.Application()
app.add_routes(routes.urls)
web.run_app(app)

config = hazelcast.ClientConfig()
config.network_config.addresses.append(settings.hazelcast_ip)
hz = hazelcast.HazelcastClient(config=config)

stat_storage = hz_get_map("stat_storage")

