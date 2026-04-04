from flask import Flask, render_template, redirect, url_for, Blueprint, request
from forms import CreateInsumoForm
from models import UnidadMedida
from . import inventario

@inventario.route('/inventario')
def index():
    unidades_medida = UnidadMedida.query.all()
    create_form = CreateInsumoForm()
    create_form.id_unidad_medida.choices = [(um.id_unidad_medida, um.nombre) for um in unidades_medida]
    return render_template('inventario/index.html', create_form=create_form)

 