from atexit import register
from random import choice, randint
from environs import ma
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, logout_user, login_required, current_user
from app.models.user.login_manager import login_manager

from app.models.user.services.auth import login, register_user
from app.models.user.services.requests import load_user

from app.config import authforms 


auth = Blueprint("auth", __name__)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/signin?next=' + request.path)

@auth.route('/signup', methods=("GET", "POST"))
def signup_route():
    if request.method == "POST":
        mes = register_user(request.form)
        if mes.show: flash(mes)
    
    return render_template("auth/form.html", form=authforms["signup"], lines=[(i, f"animation: ease-in-out infinite; animation-duration: {randint(200, 400)}s; animation-name: move_{choice([1, 2])}; height: {randint(20, 50)}") for i in range(1, 30)], circles=[(i, f"animation-duration: {randint(200, 400)}s; animation-name: rotate_{choice([1, 2])};") for i in range(1, 15)])


@auth.route('/signin', methods=("GET", "POST"))
def signin_route():
    if request.method == "POST":
        mes = login(request.form)
        if mes.type == "success":
            return redirect(url_for("main.main_route") or request.args.get('next'))

    return render_template("auth/form.html", form=authforms["signin"], lines=[(i, f"animation: ease-in-out infinite; animation-duration: {randint(200, 400)}s; animation-name: move_{choice([1, 2])}; height: {randint(20, 50)}") for i in range(1, 30)], circles=[(i, f"animation-duration: {randint(200, 400)}s; animation-name: rotate_{choice([1, 2])};") for i in range(1, 15)])