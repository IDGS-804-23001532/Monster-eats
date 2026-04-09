from string import Template
from flask import Blueprint


insumos = Blueprint('insumos', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )

from . import insumos
