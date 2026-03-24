from flask import Blueprint
from string import Template 

inventario = Blueprint('inventario', __name__,
                       template_folder='templates',
                       static_folder='static')

from . import routes