from flask import Blueprint, render_template, request, url_for, redirect
from models import Insumo   
from . import insumos


@insumos.route('/insumos')
def index():
    search_query = request.args.get('search_query', '')
    if search_query:
        # Busca coincidencias parciales sin importar mayúsculas o minúsculas
        insumos = Insumo.query.filter(Insumo.nombre.ilike(f'%{search_query}%')).all()
    else:
        insumos = Insumo.query.all()
    return render_template('insumos/index.html', insumos=insumos, search_query=search_query)

@insumos.route('/limpiar_busqueda')
def limpiar_busqueda():
    return redirect(url_for('insumos.index'))
