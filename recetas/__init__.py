from flask import Blueprint

recetas_bp = Blueprint('recetas', __name__, template_folder='templates')

from . import routes