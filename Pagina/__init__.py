from flask import Blueprint

pagina_bp = Blueprint('pagina', __name__, template_folder='templates', static_folder='static')

from . import routes
