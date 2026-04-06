from flask import Blueprint

costo_utilidad = Blueprint(
    'costo_utilidad',
    __name__,
    template_folder = 'templates',
    static_folder = 'static')
from . import routes