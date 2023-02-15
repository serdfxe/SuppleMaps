from atexit import register
from random import choice, randint
from environs import ma
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import LoginManager, logout_user, login_required, current_user
from app.models.user.login_manager import login_manager

from app.models.user.services.auth import login, register_user
from app.models.user.services.requests import load_user

from app.config import authforms 

from app.models.notification import Notification


auth = Blueprint("auth", __name__)


@login_manager.unauthorized_handler
def unauthorized_callback():
    response = jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))
    return response

@auth.post('/signup')
def signup_route():
    print(request.get_json())

    mes = register_user(request.get_json())
    
    response = jsonify(mes)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'POST')

    return response


@auth.post('/signin')
def signin_route():
        mes = login(request.get_json())
        
        response = jsonify(mes)
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'POST')
        
        return response
    
@auth.get('/is_logged_in')
def is_logged_in():
    response = jsonify(Notification("Успешно!", "Авторизован.", "success", 0, (current_user.name))) if current_user.is_authenticated else jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response

@auth.get("/user_info")
def user_info_route():
    if current_user.is_authenticated:
        response = jsonify(current_user.as_dict())
    else:
        response = jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response
