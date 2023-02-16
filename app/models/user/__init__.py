from sqlalchemy import Column, String, Integer, ForeignKey

from app.database import Base

from app.database.db_tool import DBTool


class User(Base, DBTool):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique = True)
    password_hash = Column(String(120), nullable=False) 
    style_id = Column(Integer, ForeignKey("styles.id"))


class Styles(Base, DBTool):
    __tablename__ = "styles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    tiles = Column(String(120))
    attr = Column(String(120))