from flask import Blueprint

tablero_kds = Blueprint(
    'tablero_kds',
    __name__,
    template_folder = 'templates',
    static_folder = 'static')
from . import routes