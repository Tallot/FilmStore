from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from auth import auth
from flask_login import LoginManager

from routes import main
app = Flask(__name__,template_folder="./templates")
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
from models import User
# blueprint for non-auth parts of app
from routes import main as main_blueprint
app.register_blueprint(main_blueprint)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    print(user)
    # since the user_id is just the primary key of our user table, use it in the query for the user
    # Query to Katya database,return user
    #return User.query.get(int(user_id))
    return User(1,"mail.com","1234","Max",100)


bootstrap = Bootstrap(app)
CORS(app)
if __name__ == "__main__":
    print("Server starting")
    http = WSGIServer(('0.0.0.0', 5000),app.wsgi_app)
    http.serve_forever()
