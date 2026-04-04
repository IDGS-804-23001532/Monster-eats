from flask import Blueprint, render_template, request, url_for, redirect

from . import insumos


@insumos.route('/insumos')
def index():
    return render_template('insumos/index.html')