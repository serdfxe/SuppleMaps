from urllib import response
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app

import traceback

from random import choice, randint, choices, sample

from app.models.map import *

from app.models.map.services import *
from app.models.map.services.strings import compress_desc

from app.models.map.test import *

import app.config as conf



api = Blueprint("api", __name__)


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

    d = p.as_dict()

    d["short_description"] = compress_desc(d["short_description"], 29, 3)

    response = jsonify(d)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')
    return response


@api.get("/rand_pois/<n>")
def get_rand_pois(n):
    n_of_types = len(PoiType.all())
    types = dict.fromkeys(list(range(1, n_of_types+1)))
    for i in range(1, n_of_types+1):
        types[i] = PoiType.filter(id=i).first().name

    response = jsonify([{"name": i.short_name, "type": types[i.type_id], "image": i.image.split(" ")[0], "id": i.id}  for i in sample(Poi.all(), int(n))])
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')
    return response


@api.get("/all_types")
def get_all_types():
    n_of_types = len(PoiType.all())
    types = dict.fromkeys(list(range(1, n_of_types+1)))
    for i in range(1, n_of_types+1):
        types[i] = PoiType.filter(id=i).first().name
    response = jsonify(types)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')
    return response


@api.get("/art/<id>")
def get_art(id):
    poi = Poi.filter(id=int(id)).first()
    art = {"name": poi.name, "description": poi.description, "history": poi.history}
    response = jsonify(art)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')
    return response


@api.get("/art_images/<id>")
def get_art_images(id):
    poi = Poi.filter(id=id).first()
    images = poi.image.split()
    response = jsonify(images)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')
    return response


@api.before_app_first_request
def init_matrix():
    Graph.init_graph()
    MapStyle.init_styles(conf.map_style)
