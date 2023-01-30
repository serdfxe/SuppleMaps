from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from random import randint

from app.models.map import *

from app.models.map.services import *

from app.models.map.test import *


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

@api.get("/randwayhtml")
def get_rand_way_html():
    return rand_way_in_html()