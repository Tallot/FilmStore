from flask import Blueprint, render_template, redirect, url_for, request, flash
#import rabbitmq
auth = Blueprint('auth', __name__)
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_cors import cross_origin
import requests
import os
import flask_rabbitmq
import hashlib
from models import User
users_url = "http://172.21.0.4:5000/"


@auth.route('/login', methods=["GET"])
def login():
    logout_user()
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    print("here")
    email = request.form.get('email')
    password = request.form.get('password')
    hash_pass = hashlib.md5(password.encode()).hexdigest()
    remember = True if request.form.get('remember') else False
    req_url = users_url + "signin"
    req_dict = {"mail": email,"password":hash_pass}
    resp = requests.get(req_url, json=req_dict).json()
    print(resp)
    # DB QUERY FOR USER
    # user - побудуємо якщо катя вернула ок
    user = None
    try:
        user = User(resp["id"],resp["mail"],hash_pass,resp["name"],resp["cash"])
    except:
        print("User not complete")

    if not user: #or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('routes.profile'))


@auth.route('/signup')
def signup():
    logout_user()
    return render_template("signup.html")

@auth.route('/signup', methods=["POST"])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    hash_pass = hashlib.md5(password.encode()).hexdigest()
    req_url = users_url + "signup"
    req_dict = {"mail": email, "password": hash_pass,"name":name}
    resp = requests.get(req_url, json=req_dict).json()
    if resp["error"]:
        exist = True
    else:
        exist = False

    if exist:  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Already exist")
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.

    #new_user = User(id=id,email=email, name=name, password=hash_pass)

    # add the new user to the database
    #db.session.add(new_user)
    #db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("login.html")
