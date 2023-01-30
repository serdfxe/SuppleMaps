from cgitb import html
from random import randint
import folium

import osmnx as ox

from app.models.map import *

from app.models.map.services import *


def rand_way_in_html():
    ps = set([randint(1, 105) for i in range(5)])

    try:
        pois = [Poi.filter(id=i + 1).first() for i in get_path(Graph.matrix, ps, Graph.time_list, n_of_ans=2)[0]]

        nodes = []

        for p in pois:
            n = ox.nearest_nodes(Graph.oxG, p.lon, p.lat)

            nodes.append(n)

        path = [ox.shortest_path(Graph.oxG, nodes[i - 1], nodes[i]) for i in range(1, len(nodes))][::-1]

        shortest_route_map = ox.plot_route_folium(Graph.oxG, path[0], tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png',
                attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                zoom=16)

        for r in path[1:]:
            shortest_route_map = ox.plot_route_folium(Graph.oxG, r, route_map=shortest_route_map, zoom=16)

        for p in Poi.all():#pois:
            m = folium.Marker(
                location = (p.lat, p.lon),
                popup = p.name,
                icon=folium.features.DivIcon(icon_size=(14, 14), html=f""" <div style="display: flex; flex-direction: column; align-items: center;"> <img src="http://192.168.1.67:80/static/img/markers/{p.poi_type.name}.svg"> <h1 style="font-size: 12pt">{p.name}</h1> </div> """))
                #icon=folium.features.CustomIcon(f"http://192.168.1.67:80/static/img/markers/{p.poi_type.name}.svg",
                #                      icon_size=(14, 14)))

                #icon = folium.Icon(color='red'))

            m.add_to(shortest_route_map)

        return shortest_route_map._repr_html_()
    except Exception:
        return ps