import traceback
from click import style
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import login_required, current_user

from app.models.map import *

import app.config as conf

from app.models.map.services.map import *
from app.models.map.services.strings import *


main = Blueprint("main", __name__)


@main.get("/hello-page")
def hello_page_route():
    return "Hello"

@main.get("/")
def main_route():
    return redirect("map/0")


@main.get("/map")
def map_route(id):
    m = Map.empty_map(style=MapStyle.get_all()[int(id)])

    m.add_all_pois()

    m.map.get_root().html.add_child(folium.Element(render_template("main/map/map.html", cur_page="map", sidebar=conf.side_bar_components)))

    return m.html

@main.get("/map/path")
def path_route():
    try:
        pois = tuple([int(i) for i in request.args.get("path").split(',')])
        style = int(request.args.get("style"))

        m, path, time, dist = get_map_way(pois, MapStyle.get_all()[style])

        path = [Poi.filter(id=i).first() for i in path]

        m.map.get_root().html.add_child(folium.Element(render_template("main/map/path.html", cur_page="map", sidebar=conf.side_bar_components, path=path, time=get_time_str(time), dist=get_dist_str(dist))))

        return m.html
    except Exception:
        traceback.print_exc()
        return 'Error'


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
    Graph.init_graph()
    MapStyle.init_styles(conf.map_style)
