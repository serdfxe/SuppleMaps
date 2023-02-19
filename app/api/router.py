from urllib import response
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
# from flask_login import LoginManager, logout_user, login_required, current_user

from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

import traceback

from random import choice, randint, choices, sample

from app.models.router import *
from app.models.user import *
from app.models.map.services.search import search

import json

from app.models.map.services import *

from app.models.map import *

from app.models.notification import Notification



router = Blueprint("router", __name__)


def init_user():
    user_id = User.filter(id=get_jwt_identity()).first().id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()
    return user_router


@router.get("/")
@jwt_required()
def get_router_route():
    response = jsonify(init_user().as_dict())

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response

@router.get("/search")
def search_poi():
    content = request.json
    ans = search([{"id": p.id, "name": p.name} for p in Poi.all()], content["text"])
    return json.dumps(ans)

@router.post("/add/<poi_id>")
@jwt_required()
def add_point(poi_id:str):
    if int(poi_id) > len(Poi.all()) or int(poi_id) <= 1:
        return jsonify(Notification("Ошибка!", "Некорретный id точки", "error", 1))
    
    user_router = init_user()

    if poi_id not in user_router.path.split(' '):
        #Router.update(Router.filter(owner_id=user_router.owner_id).first(), path=' '.join(curr_path + [poi_id]))
        if len(user_router.path) != 0:
            new_path = f"{user_router.path} {poi_id}"
        else:
            new_path = poi_id
        with Router.uow:
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": new_path})
            Router.uow.commit()

            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "editing"})
            Router.uow.commit()
        return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0))
    else:
        return jsonify(Notification("Ошибка!", "Точка уже есть в маршруте", "error", 1))

@router.post("/del/<poi_id>")
@jwt_required()
def delete_point(poi_id:str):
    user_router = init_user()

    if poi_id in user_router.path.split(' '):
        #Router.update(Router.filter(owner_id=user_router.owner_id).first(), path=' '.join(curr_path + [poi_id]))
        if user_router.path.startswith(poi_id+" "):
            new_path = user_router.path.replace(poi_id+" ", "")
        elif user_router.path.endswith(" "+poi_id):
            new_path = user_router.path.replace(" "+poi_id, "")
        elif user_router.path == poi_id:
            new_path = ""
        else:
            new_path = user_router.path.replace(" "+poi_id+" ", " ")
        with Router.uow:
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": new_path})
            Router.uow.commit()

            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "editing"})
            Router.uow.commit()
        return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0))
    else:
        return jsonify(Notification("Ошибка!", "Точки нет маршруте", "error", 1))
    

@router.post("/clear")
@jwt_required()
def clear_path():
    user_router = init_user()

    with Router.uow:
        Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": ""})
        Router.uow.commit()

        Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "editing"})
        Router.uow.commit()
    return jsonify(Notification("Успешно!", "Маршрут удалён", "success", 0))


@router.post("/build")
@jwt_required()
def build_path():
    user_router = init_user()

    if len(user_router.path) != 0:
        curr_path = [int(p) for p in user_router.path.split(' ')]
    else: 
        return jsonify(Notification("Ошибка!", "Пустой маршрут", "error", 1))
    
    if any(i > len(Poi.all()) or i<=1 for i in curr_path):
        return jsonify(Notification("Ошибка!", "Некорретный id точки", "error", 1))

    mtrx = Graph.matrix
    time_s = Graph.time_list

    if len(user_router.mandatory_points) != 0:
        mand_points = [int(p) for p in user_router.mandatory_points.split(' ')]
    else: 
        mand_points = []
    
    new_path = get_path(mtrx,curr_path,time_s,user_router.time_limit,mand_points,user_router.dur_of_visit,user_router.n_of_ans)[0][0]

    with Router.uow:
        Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": ' '.join([str(i) for i in new_path[1:]])})
        Router.uow.commit()

        Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "viewing"})
        Router.uow.commit()
    return jsonify(Notification("Успешно!", "Маршрут изменён", "success", 0))


@router.post("/save")
@jwt_required()
def save_path():
    user_router = init_user()

    if len(user_router.path) != 0:
        curr_path = [int(p) for p in user_router.path.split(' ')]
    else: 
        return jsonify(Notification("Ошибка!", "Пустой маршрут", "error", 1))
    
    if any(i > len(Poi.all()) or i<=1 for i in curr_path):
        return jsonify(Notification("Ошибка!", "Некорретный id точки", "error", 1))

    mtrx = Graph.matrix
    time_s = Graph.time_list

    if len(user_router.mandatory_points) != 0:
        mand_points = [int(p) for p in user_router.mandatory_points.split(' ')]
    else: 
        mand_points = []

    path, time, length = get_path(mtrx,curr_path,time_s,user_router.time_limit,mand_points,user_router.dur_of_visit,user_router.n_of_ans)[0]

    SavedPaths.new(owner_id=user_router.owner_id, name='',description='',image='',path=' '.join(str(i) for i in path[1:]),length=length,full_time=time[0], walk_time=time[1])
    return jsonify(Notification("Успешно!", "Маршрут сохранён", "success", 0))


@router.post("/loadsaved/<id>")
@jwt_required()
def load_path(id):
    user_router = init_user()
    path_id = int(id)
    if len(SavedPaths.filter(id=path_id).all()) != 0:
        if SavedPaths.filter(id=path_id).first().owner_id == user_router.owner_id:
            path = SavedPaths.filter(id=path_id).first().path
        else:
            return jsonify(Notification("Ошибка!", "Некорректный id пользователя", "error", 1))
    else:
        return jsonify(Notification("Ошибка!", "Некорректный id маршрута", "error", 1))
    
    with Router.uow:
        Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": path})
        Router.uow.commit()

        Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "viewing"})
        Router.uow.commit()
    return jsonify(Notification("Успешно!", "Маршрут загружен", "success", 0))


@router.post("/delsaved/<id>")
@jwt_required()
def delete_path(id):
    user_router = init_user()
    path_id = int(id)
    if len(SavedPaths.filter(id=path_id).all()) == 0:
        return jsonify(Notification("Ошибка!", "Некорректный id маршрута", "error", 1))
    if SavedPaths.filter(id=path_id).first().owner_id != user_router.owner_id:
        return jsonify(Notification("Ошибка!", "Некорректный id пользователя", "error", 1))
    
    SavedPaths.delete_first(id=path_id)
    return jsonify(Notification("Успешно!", "Маршрут удалён", "success", 0))
