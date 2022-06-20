import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
db = SQLAlchemy(app)

CORS(app)


from .main import blog

app.register_blueprint(blog)
