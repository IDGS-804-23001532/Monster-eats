from flask import Flask, render_template, redirect, url_for, Blueprint, request

inventario = Blueprint('inventario', __name__)

@inventario.route('/inventario')
def index():
    return render_template('inventario/index.html')

 