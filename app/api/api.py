from urllib import response
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app

from random import randint, choices

from app.models.map import *

from app.models.map.services import *

from app.models.map.test import *

import traceback

api = Blueprint("api", __name__)


@api.get("/rand_dist")
def get_random_dist_route():
    s, e = randint(1, 106), randint(1, 106)

    return f"{s} -> {e} = {Graph.distance_between(s, e)}"

@api.get("/randway")
def get_rand_way():
    pois = [randint(1, 105) for i in range(5)]

    try:

        path = "<br>".join([Poi.filter(id=i + 1).first().name for i in get_path(Graph.matrix, pois, Graph.time_list, n_of_ans=2)[0]])

        return f"""
        {pois}
        <br>
        {"; ".join([Poi.filter(id=i + 1).first().name for i in pois])}
        <br>
        <hr>
        <br>
        {path}
        <br>
        <hr>
        <br>
        {len(Graph.matrix)} {set([len(i) for i in Graph.matrix])}
        """
    except Exception:
        return pois

@api.get("/randwayhtml/<id>")
def get_rand_way_html(id):
    return rand_way_in_html(MapStyle.style_list[int(id)])

@api.get("/art/<id>")
def get_article(id):
    ln = len(Poi.all())

    if id not in ('', None) and id.isdigit() and int(id) <= ln and int(id) >= 1:
        id = int(id)
    else:
        id = randint(1, ln)

    return Poi.filter(id=id).first().description

@api.get("/wayhtml/<strpoi>")
def get_way_html(strpoi):
    try:
        poi = [int(i) for i in strpoi.split(',')]
        return way_in_html(poi, MapStyle.style_list[0])
    except Exception:
        traceback.print_exc()
        return 'Error'

@api.get("/poi_info/<id>")
def poi_info_route(id):
    p = Poi.filter(id=int(id)).first()
    return render_template("main/map/short_info.html", p=p, desc=p.description[17:217] + "...")

# API

@api.get("/rand_pois/<n>")
def get_rand_pois(n):
    response = jsonify([i.as_dict()  for i in choices(Poi.all(), k=int(n))])
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')
    return response
