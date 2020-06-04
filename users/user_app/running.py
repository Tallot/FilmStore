from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,template_folder="./templates")
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
CORS(app)

db = SQLAlchemy(app)
import routes
app.register_blueprint(routes.app)
if __name__ == "__main__":
    print("Server starting")
    http = WSGIServer(('0.0.0.0', 5000),app.wsgi_app)
    http.serve_forever()
