from . import inventario_produccion

from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime

@inventario_produccion.route('/inventario-produccion', methods=['GET', 'POST'])
def inventarioProduccioan():

    return render_template('inventario_produccion/principal.html')

@inventario_produccion.route('/combos-dinamicos', methods=['GET', 'POST'])
def combosDinamicos():

    return render_template('inventario_produccion/combosDinamicos.html')