from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Producto, Combo, DetalleCombo
from flask_security import login_required, roles_accepted
from forms import ComboForm

combos = Blueprint('combos', __name__, url_prefix='/combos')

@combos.route('/')
@login_required
@roles_accepted('administrador', 'gerente')
def principal():
    lista_combos = Combo.query.filter_by(activo=True).all()
    productos = Producto.query.filter_by(activo=True).all()
    form = ComboForm()
    return render_template('combos/principal.html', combos=lista_combos, productos=productos, form=form, edit_error_id=None)

@combos.route('/crear', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente')
def crear():
    form = ComboForm(request.form)
    lista_combos = Combo.query.filter_by(activo=True).all()
    productos = Producto.query.filter_by(activo=True).all()
    
    if form.validate():
        try:
            ids_productos = request.form.getlist('id_producto[]')
            cantidades = request.form.getlist('cantidad[]')
            productos_validos = 0
            detalles_a_guardar = []
            
            for i in range(len(ids_productos)):
                id_prod = ids_productos[i]
                cant = cantidades[i]
                if id_prod and id_prod.isdigit() and cant and cant.isdigit():
                    if int(cant) > 0:
                        detalles_a_guardar.append({'id_prod': int(id_prod), 'cant': int(cant)})
                        productos_validos += 1
            
            # Validación backend: Mínimo 2 productos
            if productos_validos < 2:
                flash('Un combo debe contener al menos 2 productos válidos.', 'error')
                return render_template('combos/principal.html', combos=lista_combos, productos=productos, form=form, edit_error_id=None)

            nuevo_combo = Combo(
                nombre=form.nombre.data, 
                descripcion=form.descripcion.data, 
                precio_venta=form.precio_venta.data
            )
            db.session.add(nuevo_combo)
            db.session.flush() 
            
            for det in detalles_a_guardar:
                detalle = DetalleCombo(
                    id_combo=nuevo_combo.id_combo,
                    id_producto=det['id_prod'],
                    cantidad=det['cant']
                )
                db.session.add(detalle)
                        
            db.session.commit()
            flash('Combo estructurado y guardado exitosamente.', 'success')
            return redirect(url_for('combos.principal'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error en combos: {e}")
            flash('Error en base de datos. Verifica que el nombre no esté repetido.', 'error')
            return redirect(url_for('combos.principal'))
            
    else:
        flash('Corrige los campos marcados en rojo.', 'error')
        return render_template('combos/principal.html', combos=lista_combos, productos=productos, form=form, edit_error_id=None)


@combos.route('/editar/<int:id_combo>', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente')
def editar(id_combo):
    form = ComboForm(request.form)
    lista_combos = Combo.query.filter_by(activo=True).all()
    productos = Producto.query.filter_by(activo=True).all()

    if form.validate():
        try:
            ids_productos = request.form.getlist('id_producto[]')
            cantidades = request.form.getlist('cantidad[]')
            productos_validos = 0
            detalles_a_guardar = []
            
            for i in range(len(ids_productos)):
                id_prod = ids_productos[i]
                cant = cantidades[i]
                if id_prod and id_prod.isdigit() and cant and cant.isdigit():
                    if int(cant) > 0:
                        detalles_a_guardar.append(DetalleCombo(
                            id_combo=id_combo,
                            id_producto=int(id_prod),
                            cantidad=int(cant)
                        ))
                        productos_validos += 1
                        
            # Validación backend: Mínimo 2 productos al editar
            if productos_validos < 2:
                flash('Error: Un combo debe contener al menos 2 productos válidos.', 'error')
                return render_template('combos/principal.html', combos=lista_combos, productos=productos, form=form, edit_error_id=id_combo)

            combo_existente = Combo.query.get_or_404(id_combo)
            combo_existente.nombre = form.nombre.data
            combo_existente.precio_venta = form.precio_venta.data
            combo_existente.descripcion = form.descripcion.data
            
            DetalleCombo.query.filter_by(id_combo=id_combo).delete()
            for det in detalles_a_guardar:
                db.session.add(det)

            db.session.commit()
            flash('Combo actualizado correctamente.', 'success')
            return redirect(url_for('combos.principal'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al editar combo: {e}")
            flash('Hubo un error al actualizar el combo.', 'error')
            return redirect(url_for('combos.principal'))
    else:
        # Si la validación de WTForms falla, regresamos el HTML con la variable edit_error_id
        flash('Corrige los errores en rojo del combo.', 'error')
        return render_template('combos/principal.html', combos=lista_combos, productos=productos, form=form, edit_error_id=id_combo)