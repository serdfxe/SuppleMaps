from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import login_required, current_user

from app.models.map import *


main = Blueprint("main", __name__)


@main.get("/hello-page")
def hello_page_route():
    return "Hello"

@main.get("/")
def main_route():
    return "Main Page!!!"

@main.get("/account")
@login_required
def account_route():
    return render_template("main/account.html")

@main.before_app_first_request
def init_matrix():
    Graph.init_graph()
