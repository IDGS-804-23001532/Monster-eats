from . import costo_utilidad

from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime

@costo_utilidad.route('/costo-utilidad', methods=['GET', 'POST'])
def costoUtilidad():

    return render_template('costo_Utilidad/principal.html')