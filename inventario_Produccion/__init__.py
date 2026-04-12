from flask import Blueprint

inventario_produccion = Blueprint(
    'inventario_produccion',
    __name__,
    template_folder = 'templates',
    static_folder = 'static')
from . import routes