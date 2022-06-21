from flask import Blueprint, request, jsonify

app = Blueprint('app', __name__, template_folder='templates', static_folder='static')
api = Blueprint('api', __name__)

from . import views


