from string import Template 
from flask import Blueprint


dasboart = Blueprint('dashboard',__name__,
                    template_folder='templates',
                    static_folder='static')

from . import routes
