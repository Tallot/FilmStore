from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify
import requests
from flask_login import login_user, logout_user, login_required,current_user
from flask import abort
main = Blueprint('routes', __name__)
import json
film_service_url = "http://172.21.0.2:8000/service_app/"
users_url = "http://172.21.0.4:5000/"
recomm_url = "http://172.21.0.6:5000/"

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/recommendations')
@login_required
def recommendations():
    req_url = recomm_url + "get_recommendations"
    resp = requests.get(req_url, json={"user_id":current_user.id}).json()["recommend"]
    return render_template("films_list.html",data = resp,enumerate=enumerate)

@main.route('/film_search')
@login_required
def film_search():
    genres = ['Documentary', 'Short', 'Animation', 'Comedy', 'Romance', 'Sport', 'Action', 'News', 'Drama', 'Fantasy',
              'Horror','Biography', 'War', 'Crime', 'Western', 'Family', 'Adventure', 'History', 'Music', 'Mystery', 'Sci-Fi']
    return render_template("film_search.html",genres=genres)


@main.route("/film_search_results",methods=["POST","GET"])
@login_required
def film_search_results():
    film_genre = request.form.get("genre")
    rating = float(request.form.get("rating")) if float(request.form.get("rating")) else "any"
    year = request.form.get("start_year") if request.form.get("start_year") else "any"
    runtime = int(request.form.get("runtime_min")) if request.form.get("runtime_min") else "any"
    is_adult = True if request.form.get("is_adult") else False
    data_for_search = {"filters": json.dumps({"is_adult":is_adult,"start_year":year,"runtime_minutes":runtime,"genres":film_genre,"average_rating":rating})}
    req_url = film_service_url + "filter"
    resp = requests.get(req_url, data_for_search).json()
    print(resp)
    if resp["success"]:
        data = resp["films"]

    return render_template("films_list.html",data = data,enumerate=enumerate)

@main.route('/feedback/<film_id>',methods=["POST"])
@login_required
def feedback(film_id):
    rating = float(request.form.get("rating"))
    req_url = film_service_url + "vote"
    req_dict = {"film_id": int(film_id),"mark":rating}
    resp = requests.get(req_url, req_dict).json()
    if resp["success"]:
        return render_template("thank_feedback.html",text="Thank you for feedback")
    else:
        return render_template("thank_feedback.html", text="Only int or float,not string,idiot")


@main.route('/find_film_by_name')
@login_required
def find_film_by_name():
    return render_template("find_film_by_name.html")

@main.route('/find_film_by_name',methods=["POST"])
@login_required
def find_film_by_name_post():
    film_title = request.form.get("film_name")
    # request to OLEG
    req_url = film_service_url+"title"
    req_dict = {"primary_title":film_title}
    resp = requests.get(req_url,req_dict).json()
    if resp["success"]:
        data = resp["films"]
    else:
        abort(404)
    return render_template("films_list.html",data=data,enumerate=enumerate)

@main.route("/single_film_info/<film_id>")
@login_required
def single_film_info(film_id):
    req_url = film_service_url + "id"
    req_dict = {"film_id": film_id}
    resp = requests.get(req_url, req_dict).json()
    if resp["success"]:
        data = resp["film"]
    return render_template("single_film_page.html",data=data)

@main.route('/add_cash',methods=["POST"])
@login_required
def add_cash():
    cash = request.form.get("cash_adding")
    # Запрос в бд Катюхи на увєлічєніє кеша
    req_url = users_url + "add_cash"
    req_dict = {"id": current_user.id,"cash":int(cash)}
    resp = requests.get(req_url, json=req_dict).json()
    print(resp)
    if resp["success"]:
        current_user.cash+=int(cash)
    return render_template("profile.html",name=current_user.name,cash=current_user.cash)


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html",name=current_user.name,cash=current_user.cash)
