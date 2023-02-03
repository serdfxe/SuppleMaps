from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import login_required, current_user

from app.models.map import *

import app.config as conf


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

@main.get("/art/<id>")
def get_article(id):
    if id != None and id.isdigit():
        p = Poi.filter(id=id).first()
        if p:
            return render_template("main/article.html", p=p, sidebar=conf.side_bar_components, cur_page="search")
        return  "Error"
    return "Error"



@main.before_app_first_request
def init_matrix():
    return
    Graph.init_graph()
    MapStyle.init_styles(conf.map_style)
