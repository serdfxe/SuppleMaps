from cgitb import html
from random import randint
import folium

import osmnx as ox
import traceback

from app.models.map import *

from app.models.map.services import *


def rand_way_in_html(style: MapStyle):
    ps = list(set([randint(1, 105) for i in range(5)]))

    try:
        pois = [Poi.filter(id=i + 1).first() for i in get_path(Graph.matrix, ps, Graph.time_list, n_of_ans=2)[0][0]]

        nodes = []

        for p in pois:
            n = ox.nearest_nodes(Graph.oxG, p.marker_lon, p.marker_lat)

            nodes.append(n)

        path = [ox.shortest_path(Graph.oxG, nodes[i - 1], nodes[i]) for i in range(1, len(nodes))][::-1]

        shortest_route_map = ox.plot_route_folium(Graph.oxG, path[0], tiles=style.tiles, attr=style.attr,
                zoom=16, max_zoom=19, min_zoom=15)

        for r in path[1:]:
            shortest_route_map = ox.plot_route_folium(Graph.oxG, r, route_map=shortest_route_map, zoom=16)

        ln = len(pois)

        for i in range(ln):
            m = folium.Marker(
                    location = (pois[i].marker_lat, pois[i].marker_lon),
                    popup = pois[i].name,
                    icon=folium.features.DivIcon(icon_size=(34, 50) if i in (0, ln - 1) else (30, 30), icon_anchor=(17, 23.5) if i in (0, ln - 1) else (15, 0), html=f""" 
                    <div style="display: flex; flex-direction: column; align-items: center;"> 
                        <img src="/static/img/markers/{i if i != 0 and i != ln - 1 else "start" if i == 0 else "end"}.svg" style="filter: drop-shadow(0px 0px 3px white);"> 
                        <h1 class="marker-text" style="transition: font-size 0.25s ease-in-out 0s, width 0.25s ease-in-out 0s;">{pois[i].short_name}</h1>
                    </div> """, class_name="marker"))

            m.add_to(shortest_route_map)


        for p in Poi.all():#pois:
            if p not in pois:
                m = folium.Marker(
                    location = (p.marker_lat, p.marker_lon),
                    popup = p.name,
                    icon=folium.features.DivIcon(icon_size=(27, 27), icon_anchor = (13.5,13.5), html=f""" 
                    <div style="display: flex; flex-direction: column; align-items: center;"> 
                        <img src="/static/img/markers/{p.poi_type.name}.svg" style="filter: drop-shadow(0px 0px 3px white);"> 
                        <h1 class="marker-text" style="transition: font-size 0.25s ease-in-out 0s, width 0.25s ease-in-out 0s;">{p.short_name}</h1>
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

        return shortest_route_map._repr_html_()
    except Exception:
        traceback.print_exc()
        return ps