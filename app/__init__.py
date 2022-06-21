import os
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

db = SQLAlchemy(app)

jwt = JWTManager(app)

from app.main import views, api
from . import view_api
from app.main import app as main_app

app.register_blueprint(main_app)
app.register_blueprint(api, url_prefix='/api')
