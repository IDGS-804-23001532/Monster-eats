from flask import Flask, render_template, redirect, url_for, Blueprint, request

from . import inventario



@inventario.route('/inventario')
def index():
    return render_template('inventario/index.html')

 