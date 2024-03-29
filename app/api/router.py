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



router = Blueprint("router", __name__)


def init_user():
    user = User.filter(id=get_jwt_identity()).first()
    user_id = user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1, length=0, full_time=0, walk_time=0) 
    user_router = Router.filter(owner_id=user_id).first()
    return user_router

def add_to_histoty(owner_id, path, length,full_time,walk_time, image):
    History.new(owner_id=owner_id, path=path, length=length, full_time=full_time, walk_time=walk_time, image = image)

@router.get("/")
@jwt_required()
def get_router_route():
    r = init_user().as_dict()

    r["path"] = [int(i) for i in r["path"].split(" ")] if r["path"] != "" else []
    r["mandatory_points"] = [int(i) for i in r["mandatory_points"].split(" ")] if r["mandatory_points"] != "" else []
    r["full_time"] = strings.get_time_str(r["full_time"])
    r["walk_time"] = strings.get_time_str(r["walk_time"])
    r["length"] = strings.get_dist_str(r["length"])
    
    response = jsonify(r)

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response

@router.post("/search")
def search_poi():
    content = request.json
    ans = search.search([{"id": p.id, "name": p.name} for p in Poi.all()], content["text"])
    return json.dumps(ans)

@router.post("/add/<poi_id>")
@jwt_required()
def add_point(poi_id:str):
    if int(poi_id) > len(Poi.all()) or int(poi_id) <= 1:
        return jsonify(Notification("Ошибка!", "Некорретный id точки", "error", 1)), 401
    
    user_router = init_user()

    if poi_id not in user_router.path.split(' '):
        #Router.update(Router.filter(owner_id=user_router.owner_id).first(), path=' '.join(curr_path + [poi_id]))
        if len(user_router.path) != 0:
            new_path = f"{user_router.path} {poi_id}"
        else:
            new_path = poi_id
        with Router.uow as u:
            u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": new_path})
            u.commit()

            u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "editing"})
            u.commit()
        return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0)), 200
    else:
        return jsonify(Notification("Ошибка!", "Точка уже есть в маршруте", "error", 1)), 401

@router.post("/del/<poi_id>")
@jwt_required()
def delete_point(poi_id:str):
    user_router = init_user()

    p =  user_router.path.split(' ')

    if poi_id in p:
        p.remove(poi_id)
        p = " ".join(p)

        mand = user_router.mandatory_points.split(' ')
        if poi_id in mand:
            mand.remove(poi_id)

        with Router.uow as u:
            u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": p})
            u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"mandatory_points": ' '. join(mand)})
            u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "editing"})
            u.commit()
        return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0))
    else:
        return jsonify(Notification("Ошибка!", "Точки нет маршруте", "error", 1))
    

@router.post("/clear")
@jwt_required()
def clear_path():
    user_router = init_user()

    with Router.uow as u:
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update(dict(state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1, length=0, full_time=0, walk_time=0))
        u.commit()
    return jsonify(Notification("Успешно!", "Маршрут удалён", "success", 0))


@router.post("/build")
@jwt_required()
def build_path():
    user_router = init_user()

    data = request.json
    print(data)

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
    print(curr_path, int(data['time_limit']), mand_points, data['dur_of_visit'], user_router.n_of_ans)
    new_path, t, length = get_path(mtrx, curr_path, time_s, int(data['time_limit']), mand_points, data['dur_of_visit'], user_router.n_of_ans)[0]
    print(new_path, t, length)
    full_time, walk_time = t
    
    with Router.uow as u:
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": ' '.join([str(i) for i in new_path[1:]])})
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"full_time": full_time})
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"walk_time": walk_time})
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"length": length})
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "viewing"})
        u.commit()
    images = [Poi.filter(id=i).first().image.split(' ') for i in new_path[1:] if Poi.filter(id=i).first().image != '']
    add_to_histoty(user_router.owner_id, ' '.join([str(i) for i in new_path[1:]]),length,full_time, walk_time, choice(choice(images)))

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
    images = [Poi.filter(id=i).first().image.split(' ') for i in path[1:] if Poi.filter(id=i).first().image != '']
    SavedPaths.new(owner_id=user_router.owner_id, name='',description='',image=choice(choice(images)),path=' '.join(str(i) for i in path[1:]),length=length,full_time=time[0], walk_time=time[1])
    return jsonify(Notification("Успешно!", "Маршрут сохранён", "success", 0))


@router.post("/loadsaved/<id>")
@jwt_required()
def load_saved(id):
    user_router = init_user()
    path_id = int(id)
    saved_paths = SavedPaths.filter(id=path_id).first()
    if saved_paths:
        if saved_paths.owner_id == user_router.owner_id:
            with Router.uow as u:
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": saved_paths.path})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"length": saved_paths.length})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"full_time": saved_paths.full_time})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"walk_time": saved_paths.walk_time})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "viewing"})
                u.commit()
            return 200
        else:
            return 400
    else:
        return 400

@router.get("/saved/")
@jwt_required()
def get_saved():
    user = User.filter(id=get_jwt_identity()).first()
    user_id = user.id

    saved = [p.as_dict() for p in SavedPaths.filter(owner_id=user_id).all()[::-1]]

    for i in range(len(saved)):
        saved[i]["path"] = [int(i) for i in saved[i]["path"].split(" ")] if saved[i]["path"] != "" else []

        saved[i]["full_time"] = strings.get_time_str(saved[i]["full_time"])
        saved[i]["walk_time"] = strings.get_time_str(saved[i]["walk_time"])
        saved[i]["length"] = strings.get_dist_str(saved[i]["length"])
    
    response = jsonify(saved)

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response, 200


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


@router.post("/loadhist/<id>")
@jwt_required()
def load_from_hist(id):
    user_router = init_user()
    path_id = int(id)
    hist = History.filter(id=path_id).first()
    if hist:
        if hist.owner_id == user_router.owner_id:
            with Router.uow as u:
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": hist.path})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"length": hist.length})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"full_time": hist.full_time})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"walk_time": hist.walk_time})
                u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "viewing"})
                u.session.commit()
            return 200
        else:
            return 400
    else:
        return 400
    
@router.post("/switchmand/<id>")
@jwt_required()
def switch_mand(id):
    user_router = init_user()
    path = [i for i in user_router.path.split(" ")] if user_router.path != "" else []
    if id not in path:
        return jsonify(Notification("Ошибка!", "Точки нет в маршруте", "error", 1))
    mand_points = [i for i in user_router.mandatory_points.split(" ")] if user_router.mandatory_points != "" else []
    if id in mand_points: mand_points.remove(id)
    else: mand_points.append(id)
    with Router.uow as u:
        u.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"mandatory_points": ' '.join(mand_points)})
        u.session.commit()
    return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0))


@router.get("/static/")
def get_static():
    stat = [p.as_dict() for p in StaticPaths.all()[::-1]]

    for i in range(len(stat)):
        stat[i]["path"] = [int(i) for i in stat[i]["path"].split(" ")] if stat[i]["path"] != "" else []

        stat[i]["full_time"] = strings.get_time_str(stat[i]["full_time"])
        stat[i]["walk_time"] = strings.get_time_str(stat[i]["walk_time"])
        stat[i]["length"] = strings.get_dist_str(stat[i]["length"])
    
    response = jsonify(stat)

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response, 200

@router.post("/loadstatic/<id>")
@jwt_required()
def load_static(id):
    user_router = init_user()
    path_id = int(id)
    stat_paths = StaticPaths.filter(id=path_id).first()
    if stat_paths:
        with Router.uow:
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"path": stat_paths.path})
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"length": stat_paths.length})
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"full_time": stat_paths.full_time})
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"walk_time": stat_paths.walk_time})
            Router.uow.session.query(Router).filter_by(owner_id = user_router.owner_id).update({"state": "viewing"})
            Router.uow.commit()
        return 200
    else:
        return 400