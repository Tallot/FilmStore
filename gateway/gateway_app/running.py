from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from flask_login import login_user, logout_user, login_required,current_user
from auth import auth
from flask_login import LoginManager
import requests
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
users_url = "http://172.21.0.4:5000/"

@login_manager.user_loader
def load_user(user):
    print(user)
    # since the user_id is just the primary key of our user table, use it in the query for the user
    # Query to Katya database,return user
    #return User.query.get(int(user_id))
    req_url = users_url + "get_info_by_id"
    req_dict = {"id": user}
    resp = requests.get(req_url, json=req_dict).json()
    print(resp)
    return User(user,resp["info"]["mail"],"pass",resp["info"]["name"],resp["info"]["cash"])
    #return current_user


bootstrap = Bootstrap(app)
CORS(app)
if __name__ == "__main__":
    print("Server starting")
    http = WSGIServer(('0.0.0.0', 5000),app.wsgi_app)
    http.serve_forever()
