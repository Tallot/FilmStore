from flask import Blueprint
#import rabbitmq
app = Blueprint("routes", __name__)
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_cors import cross_origin
import requests
import os
import json
#import flask_rabbitmq
film_service_url = "http://172.21.0.2:8000/service_app/"


@app.route('/')
def hello_world():
    return 'Hello World!'

def make_rec(user_id,full_film_db):
    return full_film_db[:10]

@app.route('/get_recommendations', methods=["GET", "POST"])
@cross_origin()
def get_recommendations():
    #with open("mongo_init_data.json",'r') as f:
    #   data = json.load(f)
    #print(data[0])
    user_id = request.json["user_id"]
    # REQ TO ANDRIY

    # RECCOMMEND FUNC
    recomm = requests.get(film_service_url+"enum").json()["ids"]
    recomm = make_rec(user_id,recomm)
    return jsonify({"recommend": recomm,"success":True})
