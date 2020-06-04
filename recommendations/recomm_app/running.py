from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import routes
app = Flask(__name__,template_folder="./templates")
app.register_blueprint(routes.app)
bootstrap = Bootstrap(app)
CORS(app)
if __name__ == "__main__":
    print("Server starting")
    http = WSGIServer(('0.0.0.0', 5000),app.wsgi_app)
    http.serve_forever()
