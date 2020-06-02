from flask import Blueprint
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, url_for, request, jsonify
main = Blueprint('routes', __name__)

correct_dict = {'title_alphanum': 'tt9999999',
                    'primary_title': 'test_title999999',
                    'is_adult': True,
                    'start_year': 1289,
                    'runtime_minutes': 13,
                    'genres': ['gg'],
                    'directors': ['wp', 'gl', 'hf'],
                    'average_rating': 6.7,
                    'num_votes': 1488,
                    "id":1}

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/recommendations')
def recommendations():
    return "RECOMMENDATIONS"

@main.route('/film_search')
def film_search():
    genres = ['Documentary', 'Short', 'Animation', 'Comedy', 'Romance', 'Sport', 'Action', 'News', 'Drama', 'Fantasy',
              'Horror','Biography', 'War', 'Crime', 'Western', 'Family', 'Adventure', 'History', 'Music', 'Mystery', 'Sci-Fi']
    return render_template("film_search.html",genres=genres)


@main.route("/film_search_results",methods=["POST","GET"])
def film_search_results():
    film_genre = request.form.get("genre")
    rating = float(request.form.get("rating"))
    year = request.form.get("start_year")
    runtime = int(request.form.get("runtime_min"))
    is_adult = True if request.form.get("is_adult") else False
    data_for_search = {"is_adult":is_adult,"start_year":year,"runtime_minutes":runtime,"genres":[film_genre],"average_rating":rating}
    # request to oleg
    # get response with film list
    temp_film_list = []
    temp_film_list.append({"id":1,"primary_title":"test"})
    temp_film_list.append({"id":2,"primary_title":"test"})
    temp_film_list.append({"id":3,"primary_title":"test"})

    return render_template("films_list.html",data = temp_film_list,enumerate=enumerate)


@main.route('/find_film_by_name')
def find_film_by_name():
    return render_template("find_film_by_name.html")

@main.route('/find_film_by_name',methods=["POST"])
def find_film_by_name_post():
    film_title = request.form.get("film_name")

    # request to OLEG
    list_with_films = [correct_dict,correct_dict]
    return render_template("films_list.html",data=list_with_films,enumerate=enumerate)

@main.route("/single_film_info/<film_id>")
def single_film_info(film_id):
    return render_template("single_film_page.html",data=correct_dict)

@main.route('/add_cash',methods=["POST"])
def add_cash():
    cash = request.form.get("cash_adding")
    # Запрос в бд Катюхи на увєлічєніє кеша
    current_user.cash+=int(cash)
    return render_template("profile.html",name=current_user.name,cash=current_user.cash)


@main.route('/profile')
def profile():
    return render_template("profile.html",name=current_user.name,cash=current_user.cash)
