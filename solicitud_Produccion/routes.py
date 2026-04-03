from . import solicitud_produccion

from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime

@solicitud_produccion.route('/solicitud-produccion', methods=['GET', 'POST'])
def solicitudProduccion():

    return render_template('solicitud_Produccion/principal.html')