from flask import Blueprint

venta = Blueprint(
    "venta",
    __name__,
    template_folder="templates/ventas",
    static_folder="static"
)

from . import routes