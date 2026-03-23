from flask import Blueprint, render_template, request, url_for, redirect


compras = Blueprint('compras',__name__)


@compras.route('/compras')
def index():
    return render_template('compras/compras.html')
