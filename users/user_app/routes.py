from flask import Blueprint

app = Blueprint("routes", __name__)
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_cors import cross_origin
from models import User
from running import db
import hashlib
@app.route("/info",methods=['GET', 'POST'])
@cross_origin()
def info():
    info = request.json['info']
    return jsonify({"success": info, "error": None})

@app.route('/signup', methods=['GET', 'POST'])
@cross_origin()
def sign_up_user():
    # try:
    mail = request.json['mail']
    print(mail)
    password = request.json['password']
    name = request.json['name']
    already_reg = User.query.filter_by(mail=mail).first()
    print(already_reg)
    if not already_reg:
        user = User(mail=mail, name=name, password=password, cash=0)
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "error": None})
        # return jsonify({"mail":mail,"userId":user.id})
    return jsonify({"success": False, "error": "Already registered"})


@app.route('/signin', methods=['GET', 'POST'])
@cross_origin()
def sign_in_user():
    mail = request.json['mail']
    password = request.json['password']
    user = User.query.filter_by(mail=mail).first()
    if user:
        if user.password == password:
            print(user)
            return jsonify({"success": True,
                            "error": None,
                            "mail": user.mail,
                            "id": user.id,
                            "cash": user.cash,
                            "name": user.name})
    return jsonify({"success": False, "error": "Wrong credentials"})
    # return jsonify({"success":False,"error": "Wrong credentials"})


@app.route('/buy', methods=['GET', 'POST'])
@cross_origin()
def buy_film():
    id = request.json["id"]
    cost = request.json["cost"]
    user = User.query.filter_by(id=id).first()
    if user.cash > cost:
        user.cash = user.cash - cost
        db.session.commit()
        # Commit to db
        return jsonify({"success": True, "error": None})
    return jsonify({"success": False, "error": "Need more cash,bro"})


@app.route('/add_cash', methods=['GET', 'POST'])
@cross_origin()
def add_cash():
    try:
        id = request.json["id"]
        cash = request.json["cash"]
        user = User.query.filter_by(id=id).first()
        user.cash = user.cash + int(cash)
        db.session.commit()
        # commit to db
        return jsonify({"success": True, "error": None})
    except:
        return jsonify({"success": False, "error": "Some troubles"})


@app.route('/get_info_by_id', methods=['GET', 'POST'])
@cross_origin()
def get_info_by_id():
    id = request.json["id"]
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({"success": True, "error": None, "info": user.serialize()})
    return jsonify({"success": False, "error": "Wrong user id"})
