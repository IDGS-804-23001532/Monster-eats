from string import Template
from flask import Blueprint 

compras = Blueprint('usuarios',__name__,
                    template_folder='templates',
                    static_folder='static')

from . import routes