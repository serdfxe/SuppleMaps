from flask import Flask

from app.api.auth import auth
from app.api.api import api
from app.api.router import router

from app.models.user.login_manager import login_manager


def create_app():
    app =  Flask(__name__)

    app.debug = 0
    app.secret_key = b"iogq3408t7h43807thirugebo8436fgy"
    
    login_manager.init_app(app)

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(router, url_prefix='/router')

    return app