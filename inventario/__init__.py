from flask import Blueprint

inventario = Blueprint('inventario', __name__,
                       template_folder='templates',
                       static_folder='static')

from . import routes