from functools import lru_cache

import folium

import osmnx as ox

from app.models.map import *

from app.models.map.services import *
from math import isnan



class Map:
    @lru_cache(10)
    def __init__(self, style=MapStyle.default, **kwargs):
        self.style = style
        self.map = folium.Map(max_bounds=True, min_lat=55.8114, max_lat=55.8534, min_lon=37.5681, max_lon=37.6726, png_enabled=True, prefer_canvas=True, tiles=style.tiles, attr=style.attr, zoom_start=16, max_zoom=19, min_zoom=15, zoom_control=False, **kwargs)
    

    @classmethod
    @lru_cache(10)
    def empty_map(cls, style=MapStyle.default, location=(55.832164, 37.628002)):
        map = Map(style=style, location=location)
        return map


    def add_extra_code(self, code):
        self.map.get_root().html.add_child(folium.Element(code))


    def add_marker(self, **kwargs):
        m = folium.Marker(**kwargs)

        m.add_to(self.map)


    def add_all_pois(self, exc: list=[]):
         for p in Poi.all():
            if p.id in exc: continue
            self.add_marker(
                location = (p.marker_lat, p.marker_lon),
                popup = p.id,
                icon=folium.features.DivIcon(icon_size=(27, 27),
                html=f"""
                    <div style="display: flex; flex-direction: column; align-items: center;"> 
                        <img src="/static/img/markers/{p.poi_type.name}.svg"> 
                        <h1 class="marker-text" style="transition: font-size 0.25s ease-in-out 0s, width 0.25s ease-in-out 0s;">{p.short_name}</h1>
                    </div> 
                """,
                class_name="marker"))


    def add_path(self, pois: list):
        pois = [Poi.filter(id=i).first() for i in pois]

        nodes = [ox.nearest_nodes(Graph.oxG, p.marker_lon, p.marker_lat) for p in pois]

        path = [ox.shortest_path(Graph.oxG, nodes[i - 1], nodes[i]) for i in range(1, len(nodes))][::-1]

        self.map = ox.plot_route_folium(Graph.oxG, path[0], route_map=self.map)

        for r in path[1:]: self.map = ox.plot_route_folium(Graph.oxG, r, route_map=self.map)

        ln = len(pois)

        for i in range(ln): 
            self.add_marker(
                location = (pois[i].marker_lat, pois[i].marker_lon),
                popup = pois[i].id,
                icon=folium.features.DivIcon(
                    icon_size=(34, 50) if i in (0, ln - 1) else (30, 30),
                    icon_anchor=(17, 23.5) if i in (0, ln - 1) else (15, 0),
                    html=f""" 
                    <div style="display: flex; flex-direction: column; align-items: center;"> 
                        <img src="/static/img/markers/{i if i != 0 and i != ln - 1 else "start" if i == 0 else "end"}.svg"> 
                        <h1 class="marker-text" style="transition: font-size 0.25s ease-in-out 0s, width 0.25s ease-in-out 0s;">{pois[i].short_name}</h1>
                    </div> """,
                    class_name="marker"
                )
            )
            if not isnan(pois[i].entrance_lat) and not isnan(pois[i].entrance_lon):
                self.add_marker(
                    location = (pois[i].entrance_lat, pois[i].entrance_lon),
                    # popup = pois[i].name,
                    icon=folium.features.DivIcon(
                        icon_size= (15, 15),
                        icon_anchor= (7.5, 7.5),
                        html=f""" 
                        <div style="display: flex; flex-direction: column; align-items: center;"> 
                            <img src="/static/img/markers/entrance.svg"> 
                        </div> """,
                        class_name="marker"
                    )
                )

        self.add_all_pois([p.id for p in pois])


    @property
    def html(self):

        mapJsVar = self.map.get_name()

        code = """
        <style>
        .leaflet-marker-icon {
            transition: font-size 0.25s;
        }
        .marker {
            white-space: nowrap;
            color:k;
            font-size:12pt;
        }
        """ + self.style.css + """
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
                var mapZoom = {map}.getZoom();
                console.log(mapZoom);
                
                $(".marker-text").css("font-size", fontSizeFromZoom(mapZoom));
                $(".marker-text").css("width", widthFromZoom(mapZoom));
                if (mapZoom <= 16) {
                    $(".marker-text").css("font-size", "0");
                    $(".marker-text").css("width", "0");
                }
            }
            updateTextSizes();
            {map}.on("zoomend", updateTextSizes);
        }
        </script>
        """.replace("{map}", mapJsVar)

        self.add_extra_code(code)

        return self.map.get_root().render()
        return self.map._repr_html_()


@lru_cache(100)
def get_map_way(pois, style=MapStyle.default):
    m = Map.empty_map(style=style)

    m.add_path(get_path(Graph.matrix, pois, Graph.time_list, n_of_ans=2)[0][0])

    return m.html


@lru_cache(1)
def get_empty_map(style=MapStyle.default):
    m = Map.empty_map(style=style)

    m.add_all_pois()

    return m.html
