from flask import Blueprint

solicitud_produccion = Blueprint(
    'solicitud_produccion',
    __name__,
    template_folder = 'templates',
    static_folder = 'static')
from . import routes