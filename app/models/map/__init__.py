import zlib, base64

import osmnx as ox

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base

from app.database.db_tool import DBTool


class Poi(Base, DBTool):
    __tablename__ = "poi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)
    image = Column(String(120), nullable=False, unique=True)
    description = Column(Text(5000), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey("poi_type.id"), nullable=False)
    time = Column(Integer, nullable=False)

    poi_type = relationship("PoiType")

    @classmethod
    def compress(cls, s: str) -> str:
        return base64.b64encode(zlib.compress(s.encode("utf-8")))

    @classmethod
    def decompress(cls, s: str) -> str:
        return zlib.decompress(base64.b64decode(s)).decode("utf-8")


class DistanceList(Base, DBTool):
    __tablename__ = "distance_list"

    start_id = Column(Integer, primary_key=True)
    end_id = Column(Integer, primary_key=True)
  
    distance = Column(Integer, nullable=False)


class PoiType(Base, DBTool):
    __tablename__ = "poi_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)


class Graph():
    @classmethod
    def init_matrix(cls):
        pois_count = len(Poi.all())

        m = [[0] * pois_count for i in range(pois_count)]

        for i in range(0, pois_count):
            for ii in range(0, pois_count):
                m[i][ii] = DistanceList.filter(start_id=i + 1, end_id=ii + 1).first().distance
        

        cls.matrix = m

    @classmethod
    def init_time_list(cls):
        pois_count = len(Poi.all())

        l = []

        for i in range(0, pois_count):
            l.append(Poi.filter(id=i + 1).first().time)
        
        cls.time_list = l

    @classmethod
    def init_ox(cls):
        #cls.oxG = ox.graph_from_place('VDNH, Russia', network_type='walk')
        cls.oxG =  ox.graph_from_bbox(55.8475, 55.8206, 37.5798, 37.6505, network_type='walk')

    @classmethod
    def init_graph(cls):
        cls.init_ox()
        cls.init_matrix()
        cls.init_time_list()

    @classmethod
    def distance_between(cls, start_point, end_point):
        return cls.matrix[start_point - 1][end_point - 1], DistanceList.filter(start_id=start_point, end_id=end_point).first().distance

class MapStyles():
    # = {'tiles':'', 'attr':''}
    voyager_nolabels = {"tiles":'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', "attr":'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'}
    thunderforest_outdoorss = {'tiles':'https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=b2657f580b7c4e5c9832cf371031763a', 'attr':'&copy; <a href="http://www.thunderforest.com/%22%3EThunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright%22%3EOpenStreetMap</a> contributors'}
    satellite = {'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 'attr': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'}

    topo = {'tiles': 'https://api.maptiler.com/maps/topo-v2/{z}/{x}/{y}@2x.png?key=HE0hiltCVg2gETfdEctd', 'attr': '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'}

    streets = {"tiles": "https://api.maptiler.com/maps/streets-v2/256/{z}/{x}/{y}@2x.png?key=HE0hiltCVg2gETfdEctd", "attr": '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'}

    style_list = [voyager_nolabels, thunderforest_outdoorss, satellite, topo, streets]
