from flask import Blueprint, render_template, redirect, url_for, request, flash
#import rabbitmq
auth = Blueprint('auth', __name__)
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_cors import cross_origin
import requests
import os
import flask_rabbitmq
from models import User

def make_rec(user_id,full_film_db):
    pass


@auth.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    print("here")
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Реквест до Каті, єслі ок - вертає юзер айді i юзернейм,єслі нєт - вертає флаг "error"=True
    #user = User.query.filter_by(email=email).first()

    # DB QUERY FOR USER
    # user - побудуємо якщо катя вернула ок
    user = User(1,"mail.com","1234","Max",cash=100)
    # IF USER NOT NONE - return user mail and hash_pass

    if not user: #or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('routes.profile'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=["POST"])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    hash_pass = generate_password_hash(password, method='sha256')
    # Отправляю Каті email,name,hash_pass - отримую або айді чєла,або то шо мейл вже існує(поле exist=True)

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
def logout():
    return render_template("login.html")
