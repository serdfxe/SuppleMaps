from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import jwt_manager

from app.api.auth import auth
from app.api.api import api
from app.api.router import router
from app.api.map import map
from app.api.history import history

# from app.models.user.login_manager import login_manager
from app.models.user.jwt_manager import jwt

from app.app import app


def create_app():
    app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    app.debug = 0
    app.secret_key = b"iogq3408t7h43807thirugebo8436fgy"
    
    jwt.init_app(app)

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(router, url_prefix='/router')
    app.register_blueprint(map, url_prefix='/map')
    app.register_blueprint(history, url_prefix='/history')

    CORS(app, supports_credentials=True) 

    return app

