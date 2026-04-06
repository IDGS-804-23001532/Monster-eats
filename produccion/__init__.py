from flask import Blueprint

produccion_bp = Blueprint('produccion', __name__, template_folder='templates')

from . import routes