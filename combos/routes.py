from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Producto, Combo, DetalleCombo
from flask_security import login_required, roles_accepted
from forms import ComboForm

combos = Blueprint('combos', __name__, url_prefix='/combos')

@combos.route('/')
@login_required
@roles_accepted('administrador', 'gerente')
def principal():
    combos = Combo.query.filter_by(activo=True).all()
    productos = Producto.query.filter_by(activo=True).all()
    
    # Instanciamos el nuevo formulario
    form = ComboForm()
    
    return render_template('combos/principal.html', combos=combos, productos=productos, form=form)

@combos.route('/crear', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente')
def crear():
    form = ComboForm(request.form)
    
    # 1. Validamos la cabecera (Tabla 'combos') con la seguridad de WTForms
    if form.validate():
        try:
            # Los nombres coinciden perfecto con la BD y el Form
            nuevo_combo = Combo(
                nombre=form.nombre.data, 
                descripcion=form.descripcion.data, 
                precio_venta=form.precio_venta.data
            )
            db.session.add(nuevo_combo)
            db.session.flush() # Obtenemos el ID del combo recién creado
            
            # 2. Leemos los detalles (Tabla 'detalle_combos') directamente del request
            ids_productos = request.form.getlist('id_producto[]')
            cantidades = request.form.getlist('cantidad[]')
            
            for i in range(len(ids_productos)):
                id_prod = ids_productos[i]
                cant = cantidades[i]
                
                # Filtramos para no guardar campos vacíos del HTML
                if id_prod and id_prod.isdigit() and cant and cant.isdigit():
                    if int(cant) > 0:
                        detalle = DetalleCombo(
                            id_combo=nuevo_combo.id_combo,
                            id_producto=int(id_prod),
                            cantidad=int(cant)
                        )
                        db.session.add(detalle)
                        
            db.session.commit()
            flash('Combo estructurado y guardado exitosamente.', 'success')
            
        except Exception as e:
            db.session.rollback()
            print(f"Error en combos: {e}")
            flash('Error al crear el combo. Verifica que el nombre no esté repetido.', 'error')
    else:
        # Mostramos los errores si el usuario se saltó la validación (ej. precio negativo)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en {getattr(form, field).label.text}: {error}", 'error')
                
    return redirect(url_for('combos.principal'))