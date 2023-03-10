import pickle
import zlib, base64
from environs import functools
from itsdangerous import exc

import osmnx as ox

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.database import Base

from app.database.db_tool import DBTool

class Router(Base, DBTool):
    __tablename__ = "router"

    owner_id = Column(Integer, ForeignKey("poi.id"), primary_key=True, nullable=False)
    state = Column(String(50))
    path = Column(String(100))
    time_limit = Column(Integer)
    mandatory_points = Column(String(100))
    dur_of_visit = Column(Boolean)
    n_of_ans = Column(Integer)
    length = Column(Integer)
    full_time = Column(Integer)
    walk_time = Column(Integer)

class History(Base, DBTool):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("poi.id"), nullable=False)
    path = Column(String(100))
    length = Column(Integer)
    full_time = Column(Integer)
    walk_time = Column(Integer)
    image = Column(String(120))