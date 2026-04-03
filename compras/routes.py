from flask import Blueprint, render_template, request, url_for, redirect


from . import compras

@compras.route('/compras')
def index():
    return render_template('compras/index.html')
