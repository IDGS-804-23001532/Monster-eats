from flask import Blueprint, render_template, request, url_for, redirect


compras = Blueprint('usuarios',__name__)

@compras.route('/usuarios')
def index():
    return render_template('usuarios/index.html')