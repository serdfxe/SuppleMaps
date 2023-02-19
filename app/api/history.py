from urllib import response
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
# from flask_login import LoginManager, logout_user, login_required, current_user

from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

import traceback

from random import choice, randint, choices, sample
from app.models.map.services import strings

from app.models.router import *
from app.models.user import *
import app.models.map.services.search as search

import json

from app.models.map.services import *

from app.models.map import *

from app.models.notification import Notification



history = Blueprint("history", __name__)

def init_user():
    user = User.filter(id=get_jwt_identity()).first()
    user_id = user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1, length=0, full_time=0, walk_time=0) 
    user_router = Router.filter(owner_id=user_id).first()
    return user_router


@history.get("/")
@jwt_required()
def get_history():
    user = User.filter(id=get_jwt_identity()).first()
    user_id = user.id

    hist = [p.as_dict() for p in History.filter(owner_id=user_id).all()]

    for i in range(len(hist)):
        hist[i]["path"] = [int(i) for i in hist[i]["path"].split(" ")[::-1]] if hist[i]["path"] != "" else []

        hist[i]["full_time"] = strings.get_time_str(hist[i]["full_time"])
        hist[i]["walk_time"] = strings.get_time_str(hist[i]["walk_time"])
        hist[i]["length"] = strings.get_dist_str(hist[i]["length"])
    
    response = jsonify(hist)

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response, 200

