import traceback
from click import style
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from flask_login import login_required, current_user

from app.models.map import *

import app.config as conf

from app.models.map.services.map import *
from app.models.map.services.strings import *
from app.models.user import User
from app.models.router import Router


map = Blueprint("map", __name__)

@map.get("/")
@jwt_required()
def map_route():
    user = User.filter(id=get_jwt_identity()).first()
    user_id = user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()
    print(user_router.path)
    m = Map.empty_map(style=MapStyle.get_all()[user.style_id if user.style_id != None else 0])
    if user_router.state == 'editing':
        m.add_all_pois()
    else:
        m.add_path([1]+[int(i) for i in user_router.path.split(' ')])
        
    # with open("index.html", 'w') as f:
    #     f.write(m.html)
    response = jsonify({"map": m.html})

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response