from cgitb import html
from random import randint
import folium

import osmnx as ox

from app.models.map import *

from app.models.map.services import *


def rand_way_in_html(style: dict):
    ps = set([randint(1, 105) for i in range(5)])

    try:
        pois = [Poi.filter(id=i + 1).first() for i in get_path(Graph.matrix, ps, Graph.time_list, n_of_ans=2)[0]]

        nodes = []

        for p in pois:
            n = ox.nearest_nodes(Graph.oxG, p.lon, p.lat)

            nodes.append(n)

        path = [ox.shortest_path(Graph.oxG, nodes[i - 1], nodes[i]) for i in range(1, len(nodes))][::-1]

        shortest_route_map = ox.plot_route_folium(Graph.oxG, path[0], **style,
                zoom=16, max_zoom=19, min_zoom=15)

        for r in path[1:]:
            shortest_route_map = ox.plot_route_folium(Graph.oxG, r, route_map=shortest_route_map, zoom=16)

        for p in Poi.all():#pois:
            m = folium.Marker(
                location = (p.lat, p.lon),
                popup = p.name,
                icon=folium.features.DivIcon(icon_size=(14, 14), html=f""" 
                <div style="display: flex; flex-direction: column; align-items: center;"> 
                    <img src="http://192.168.1.67:80/static/img/markers/{p.poi_type.name}.svg"> 
                    <h1 class="marker-text">{p.name}</h1>
                </div> """, class_name="marker"))
                #icon=folium.features.CustomIcon(f"http://192.168.1.67:80/static/img/markers/{p.poi_type.name}.svg",
                #                      icon_size=(14, 14)))

                #icon = folium.Icon(color='red'))

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

        .marker-text {
            white-space: break-spaces;
            width: 
            color:k;
            font-size:12pt;
            transition: font-size 0.25s;
            transition: width 0.25s;
            text-align: center;
        }
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
                    $(".marker-text").css("display", "none");
                } else {
                    $(".marker-text").css("display", "block");
                }
            }
            updateTextSizes();
            {shortest_route_map}.on("zoomend", updateTextSizes);
        }
        </script>
        """.replace("{shortest_route_map}", mapJsVar)))

        return shortest_route_map._repr_html_()
    except Exception:
        return ps