from flask import Blueprint

combos = Blueprint('combos',__name__,
                    template_folder='templates',
                    static_folder='static')

from . import routes