from urllib import response
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, logout_user, login_required, current_user
import traceback

from random import choice, randint, choices, sample

from app.models.router import *
from app.models.user import *

from app.models.map.services import *

from app.models.map import *

from app.models.notification import Notification



router = Blueprint("router", __name__)


@router.get("/add/<poi_id>")
@login_required
def add_point(poi_id:str):
    if int(poi_id) > len(Poi.all()) or int(poi_id) <= 1:
        return jsonify(Notification("Ошибка!", "Некорретный id точки", "error", 1))

    user_id = current_user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()

    if poi_id not in user_router.path.split(' '):
        #Router.update(Router.filter(owner_id=user_id).first(), path=' '.join(curr_path + [poi_id]))
        if len(user_router.path) != 0:
            new_path = f"{user_router.path} {poi_id}"
        else:
            new_path = poi_id
        with Router.uow:
            Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"path": new_path})
            Router.uow.commit()

            Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"state": "editing"})
            Router.uow.commit()
        return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0))
    else:
        return jsonify(Notification("Ошибка!", "Точка уже есть в маршруте", "error", 1))
    
@router.get("/del/<poi_id>")
@login_required
def delete_point(poi_id:str):
    user_id = current_user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()

    if poi_id in user_router.path.split(' '):
        #Router.update(Router.filter(owner_id=user_id).first(), path=' '.join(curr_path + [poi_id]))
        if user_router.path.startswith(poi_id+" "):
            new_path = user_router.path.replace(poi_id+" ", "")
        elif user_router.path.endswith(" "+poi_id):
            new_path = user_router.path.replace(" "+poi_id, "")
        elif user_router.path == poi_id:
            new_path = ""
        else:
            new_path = user_router.path.replace(" "+poi_id+" ", " ")
        with Router.uow:
            Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"path": new_path})
            Router.uow.commit()

            Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"state": "editing"})
            Router.uow.commit()
        return jsonify(Notification("Успешно!", "Маршрут обновлён", "success", 0))
    else:
        return jsonify(Notification("Ошибка!", "Точки нет маршруте", "error", 1))
    
@router.get("/clear")
@login_required
def clear_path():
    user_id = current_user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()

    with Router.uow:
        Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"path": ""})
        Router.uow.commit()

        Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"state": "editing"})
        Router.uow.commit()
    return jsonify(Notification("Успешно!", "Маршрут удалён", "success", 0))

@router.get("/build")
@login_required
def build_path():
    user_id = current_user.id
    ids = [u.owner_id for u in Router.all()]
    if user_id not in ids:
        Router.new(owner_id=user_id, state="editing", path="", time_limit=10**5, mandatory_points="", dur_of_visit=False, n_of_ans=1)
    user_router = Router.filter(owner_id=user_id).first()

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
        Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"path": ' '.join([str(i) for i in new_path[1:]])})
        Router.uow.commit()

        Router.uow.session.query(Router).filter_by(owner_id = user_id).update({"state": "viewing"})
        Router.uow.commit()
    return jsonify(Notification("Успешно!", "Маршрут изменён", "success", 0))

