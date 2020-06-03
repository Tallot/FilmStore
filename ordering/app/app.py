import routes
import settings
import hazelcast
from aiohttp import web

app = web.Application()
app.add_routes(routes.urls)
web.run_app(app)

