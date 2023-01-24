from sqlalchemy import Column, String, Integer

from app.database import Base

from flask_login import UserMixin

from app.database.db_tool import DBTool


class User(UserMixin, Base, DBTool):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique = True)
    password_hash = Column(String(120), nullable=False)
