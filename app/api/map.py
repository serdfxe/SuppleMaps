import traceback
from click import style
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from flask_login import login_required, current_user

from app.models.map import *

import app.config as conf

from app.models.map.services.map import *
from app.models.map.services.strings import *
from app.models.user import User
from app.models.router import Router


def path_map(pois:list, style: MapStyle):
    try:
        pois = [Poi.filter(id=i).first() for i in pois]

        nodes = []

        for p in pois:
            n = ox.nearest_nodes(Graph.oxG, p.marker_lon, p.marker_lat)

            nodes.append(n)

        path = [ox.shortest_path(Graph.oxG, nodes[i - 1], nodes[i]) for i in range(1, len(nodes))][::-1]

        fmap = folium.Map(tiles=style.tiles, attr=style.attr, zoom_start=18, max_zoom=19, min_zoom=15, zoom_control=False)

        shortest_route_map = ox.plot_route_folium(Graph.oxG, path[0], route_map=fmap, zoom = 18)

        for r in path[1:]:
            shortest_route_map = ox.plot_route_folium(Graph.oxG, r, route_map=shortest_route_map, zoom=18)

        ln = len(pois)

        for i in range(ln):
            m = folium.Marker(
                    location = (pois[i].marker_lat, pois[i].marker_lon),
                    popup = pois[i].name,
                    icon=folium.features.DivIcon(icon_size=(34, 50) if i in (0, ln - 1) else (30, 30), icon_anchor=(17, 23.5) if i in (0, ln - 1) else (15, 0), html=f""" 
                    <div style="display: flex; flex-direction: column; align-items: center;"> 
                        <img src="http://localhost:80/static/img/markers/{i if i != 0 and i != ln - 1 else "start" if i == 0 else "end"}.svg" style="filter: drop-shadow(0px 0px 3px white);"> 
                        <h1 class="marker-text" style="transition: font-size 0.25s ease-in-out 0s, width 0.25s ease-in-out 0s;">{pois[i].short_name}</h1>
                    </div> """, class_name="marker"))

            m.add_to(shortest_route_map)


        for p in Poi.all():#pois:
            if p not in pois:
                m = folium.Marker(
                    location = (p.marker_lat, p.marker_lon),
                    popup = p.name,
                    icon=folium.features.DivIcon(icon_size=(27, 27), html=f""" 
                    <div style="display: flex; flex-direction: column; align-items: center;"> 
                        <img src="http://localhost:80/static/img/markers/{p.poi_type.name}.svg" style="filter: drop-shadow(0px 0px 3px white);"> 
                        <h1 class="marker-text" style="transition: font-size 0.25s ease-in-out 0s, width 0.25s ease-in-out 0s;">{p.short_name}</h1>
                    </div> """, class_name="marker"))
                m.add_to(shortest_route_map)

        mapJsVar = shortest_route_map.get_name()

        shortest_route_map.get_root().html.add_child(folium.Element("""
        <style>
        .leaflet-marker-icon {
            transition: font-size 0.25s;
        }
        .marker {
            white-space: nowrap;
            color:k;
            font-size:12pt;
        }
        """ + style.css + """
        </style>
        <script type="text/javascript">
        window.onload = function(){
            var fontSizeFromZoom = function(z){
                return {17: 11, 18: 18, 19: 29}[z]
            }
            var widthFromZoom = function (z) {
                return {17: 95, 18: 155, 19: 250}[z]
            }
            var updateTextSizes = function(){
                var mapZoom = {shortest_route_map}.getZoom();
                console.log(mapZoom);
                
                $(".marker-text").css("font-size", fontSizeFromZoom(mapZoom));
                $(".marker-text").css("width", widthFromZoom(mapZoom));
                if (mapZoom <= 16) {
                    $(".marker-text").css("font-size", "0");
                    $(".marker-text").css("width", "0");
                }
            }
            updateTextSizes();
            {shortest_route_map}.on("zoomend", updateTextSizes);
        }
        </script>
        """.replace("{shortest_route_map}", mapJsVar)))

        return shortest_route_map
    except Exception:
        traceback.print_exc()
        return pois

map = Blueprint("map", __name__)

def init_user():
    user_id = User.filter(id=get_jwt_identity()).first().id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()
    return user_router

@map.get("/")
@jwt_required()
def map_route():
    user = User.filter(id=get_jwt_identity()).first()
    user_router = init_user()
    if user_router.state == 'editing':
        m = Map.empty_map(style=MapStyle.get_all()[user.style_id if user.style_id != None else 0])
        m.add_all_pois()
        response = jsonify({"map": m.html})
    else:
        print([int(i) for i in user_router.path.split(' ')])
        m = path_map([1] + [int(i) for i in user_router.path.split(' ')], MapStyle.style_list[user.style_id if user.style_id != None else 0])
        response = jsonify({"map": m._repr_html_()})

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response