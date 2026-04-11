from flask import Blueprint

mermas = Blueprint('mermas', __name__, template_folder='templates')

from . import routes
