from flask import Blueprint

recetas_bp = Blueprint('recetas', __name__, template_folder='templates', static_folder='static')

from . import routes