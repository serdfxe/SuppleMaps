from atexit import register
import datetime
import json
from random import choice, randint
from environs import ma
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from app.models.user import User
# from flask_login import LoginManager, logout_user, login_required, current_user
from app.models.user.login_manager import login_manager

from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager


from app.models.user.services.auth import check_password, register_user
from app.models.user.services.requests import load_user

from app.config import authforms 

from app.models.notification import Notification


auth = Blueprint("auth", __name__)


@auth.post('/token')
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    c = check_password(email, password)
    if not c[0]:
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=c[1])
    
    response = jsonify({"token": access_token})
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'POST')

    return response


@auth.post("/logout")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@auth.route('/profile')
@jwt_required()
def my_profile():
    user = User.filter(id=get_jwt_identity()).first()
    
    if user:
        d = user.as_dict()
        resp = {i: d[i] for i in d if i != "password_hash"}
        response = (jsonify(resp), 200)
    else:
        response = (Notification("Ошибка!", "Не авторизован!", "error", 0), 401)

    return response


@auth.post('/reg')
def reg_route():
    print(request.get_json())

    mes = register_user(request.get_json())
    
    response = jsonify(mes)

    if mes.type == "success":
        access_token = create_access_token(identity=mes.content[0])
        
        response = jsonify({"token": access_token})
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'POST')

    return response

    
# @auth.route('/logout', methods=["POST"])
# @login_required
# def logout():
#     logout_user()
#     return jsonify(Notification("Успешно!", "Вы вышли из аккаунта", "success", 0))
    
# @auth.post('/isloggedin')
# def is_logged_in():
#     response = jsonify(Notification("Успешно!", "Авторизован.", "success", 0, (current_user.name))) if current_user.is_authenticated else jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))
#     response.headers.set('Access-Control-Allow-Origin', '*')
#     response.headers.set('Access-Control-Allow-Methods', 'GET')

#     return response

# @auth.get("/user_info")
# def user_info_route():
#     if current_user.is_authenticated:
#         response = jsonify(current_user.as_dict())
#     else:
#         response = jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))
#     response.headers.set('Access-Control-Allow-Origin', '*')
#     response.headers.set('Access-Control-Allow-Methods', 'GET')

#     return response
