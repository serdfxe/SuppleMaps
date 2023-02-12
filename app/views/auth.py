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
    return jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))


@auth.post('/signup')
def signup_route():
    mes = register_user(request.get_json())
    
    return jsonify(mes)


@auth.route('/signin', methods=("GET", "POST"))
def signin_route():
    if request.method == "POST":
        mes = login(request.get_json())
        return jsonify(mes)
    
@auth.post('/is_logged_in')
def is_logged_in():
    if current_user.is_authenticated:
        return jsonify(Notification("Успешно!", "Авторизован.", "success", 0))
    else:
        return jsonify(Notification("Ошибка!", "Не авторизован.", "error", 1))