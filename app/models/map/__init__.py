import pickle
import zlib, base64
from environs import functools
from itsdangerous import exc

import osmnx as ox

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base

from app.database.db_tool import DBTool


class Poi(Base, DBTool):
    __tablename__ = "poi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)
    short_name = Column(String(120))
    image = Column(String(1000), nullable=False, unique=True)
    description = Column(String(7000))
    short_description = Column(String(1000))
    history = Column(String(20000))
    entrance_lat = Column(Float)
    entrance_lon = Column(Float)    
    type_id = Column(Integer, ForeignKey("poi_type.id"), nullable=False)
    time = Column(Integer, nullable=False)
    marker_lat = Column(Float)
    marker_lon = Column(Float)

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



class StaticPaths(Base, DBTool):
    __tablename__ = "static_paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)
    description = Column(String(5000), nullable=False)
    image = Column(String(120), nullable=False)
    path = Column(String(120), nullable=False)
    lenght = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)


class SavedPaths(Base, DBTool):
    __tablename__ = "saved_paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(120), nullable=False, unique=True)
    description = Column(String(5000), nullable=False)
    image = Column(String(120), nullable=False)
    path = Column(String(120), nullable=False)
    lenght = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)


class Graph():
    @classmethod
    def init_matrix(cls):
        try:
            cls.matrix = pickle.load(open("app/models/map/serialized_objs/matrix.txt", "rb"))
        except Exception:
            pois_count = len(Poi.all())

            m = [[0] * pois_count for i in range(pois_count)]

            for i in range(0, pois_count):
                for ii in range(0, pois_count):
                    m[i][ii] = DistanceList.filter(start_id=i + 1, end_id=ii + 1).first().distance
                
            cls.matrix = m

            pickle.dump(cls.matrix, open("app/models/map/serialized_objs/matrix.txt", "wb"))

    @classmethod
    def init_time_list(cls):
        try:
            cls.time_list = pickle.load(open("app/models/map/serialized_objs/time_list.txt", "rb"))
        except Exception:
            pois_count = len(Poi.all())

            l = []

            for i in range(0, pois_count):
                l.append(Poi.filter(id=i + 1).first().time)
            
            cls.time_list = l

            pickle.dump(cls.time_list, open("app/models/map/serialized_objs/time_list.txt", "wb"))

    @classmethod
    def init_ox(cls):
        try:
            cls.oxG = pickle.load(open("app/models/map/serialized_objs/oxG.txt", "rb"))
        except Exception:
            cls.oxG =  ox.graph_from_bbox(55.8475, 55.8206, 37.5798, 37.6505, network_type='walk')
            pickle.dump(cls.oxG, open("app/models/map/serialized_objs/oxG.txt", "wb"))

    @classmethod
    def init_graph(cls):
        cls.init_ox()
        cls.init_matrix()
        cls.init_time_list()

    @classmethod
    def distance_between(cls, start_point, end_point):
        return cls.matrix[start_point - 1][end_point - 1], DistanceList.filter(start_id=start_point, end_id=end_point).first().distance


class MapStyle():
    # = {'tiles':'', 'attr':''}
    default_css = """
    .marker-text {
            white-space: break-spaces;
            font-size:11pt;
            transition: font-size 0.25s;
            transition: width 0.25s;
            text-align: center;
            -moz-text-shadow:0 0 10px #c00; -webkit-text-shadow:0 0 10px #c00; text-shadow:0 0 10px white;
            color: #101727;
            font-weight: 700;
        }
    """

    style_list = []
    default = None

    def __init__(self, tiles: str, attr: str, css=default_css):
        self.tiles = tiles
        self.attr = attr

        self.css = css

    @classmethod
    def get_all(cls):
        return cls.style_list

    @classmethod
    def init_styles(cls, styles: dict):
        for s in styles:
            new = cls(**styles[s])
            cls.style_list.append(new)
        cls.default = cls.style_list[0]
