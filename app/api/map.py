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



map = Blueprint("map", __name__)


@map.get("/empty")
@jwt_required()
def map_route():
    user = User.filter(id=get_jwt_identity()).first()

    m = Map.empty_map(style=MapStyle.get_all()[user.style_id if user.style_id != None else 0])

    m.add_all_pois()

    response = jsonify({"map": m.html})
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response
