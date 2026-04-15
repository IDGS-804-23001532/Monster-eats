import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from models import db, Producto, Combo, DetalleCombo
from flask_security import login_required, roles_accepted
from forms import ComboForm
from sqlalchemy import text

combos = Blueprint('combos', __name__, url_prefix='/combos')

@combos.route('/')
@login_required
@roles_accepted('administrador', 'gerente')
def principal():
    search_query = request.args.get('q', '').strip()
    
    # 2. Consultamos la tabla original 'combos' (trae activos e inactivos)
    if search_query:
        sql = text("SELECT * FROM combos WHERE LOWER(nombre) LIKE :search")
        lista_combos = Combo.query.from_statement(sql).params(search=f"%{search_query.lower()}%").all()
    else:
        sql = text("SELECT * FROM combos")
        lista_combos = Combo.query.from_statement(sql).all()
        
    productos = Producto.query.filter_by(activo=True).all()
    
    return render_template('combos/principal.html', combos=lista_combos, productos=productos, form=ComboForm(), form_edit=ComboForm(), edit_error_id=None)

@combos.route('/toggle_estado/<int:id_combo>', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente')
def toggle_estado(id_combo):
    try:
        # Usamos SQL directo para invertir el valor de activo (1 pasa a 0, 0 pasa a 1)
        db.session.execute(
            text("UPDATE combos SET activo = NOT activo WHERE id_combo = :id"),
            {"id": id_combo}
        )
        db.session.commit()
        flash('El estado del combo ha sido actualizado.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error al cambiar estado: {e}")
        flash('Error al cambiar el estado del combo.', 'error')
    return redirect(url_for('combos.principal'))

@combos.route('/crear', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente')
def crear():
    form = ComboForm(request.form)
    
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
            
            if productos_validos < 2:
                flash('Un combo debe contener al menos 2 productos válidos.', 'error')
                return redirect(url_for('combos.principal'))

            # ----- LÓGICA PARA GUARDAR IMAGEN -----
            imagen_file = request.files.get('imagen')
            nombre_imagen = 'Combo.png' # Valor por defecto si no suben nada

            if imagen_file and imagen_file.filename != '':
                # Limpiamos el nombre del archivo y lo guardamos en /static/img/
                filename = secure_filename(imagen_file.filename)
                filepath = os.path.join(current_app.root_path, 'static', 'img', filename)
                imagen_file.save(filepath)
                nombre_imagen = filename
            # --------------------------------------

            # 1. EJECUTAR SP PARA CREAR INFO DEL COMBO
            db.session.execute(
                text("CALL sp_crear_combo(:nombre, :desc, :precio, :img, @out_id)"),
                {
                    "nombre": form.nombre.data, 
                    "desc": form.descripcion.data, 
                    "precio": form.precio_venta.data, 
                    "img": nombre_imagen
                }
            )
            
            # 2. Atrapamos el ID generado por el OUT_PARAMETER del SP
            res = db.session.execute(text("SELECT @out_id")).fetchone()
            nuevo_id_combo = res[0]
            
            # 3. EJECUTAR SP PARA CREAR LOS DETALLES
            for det in detalles_a_guardar:
                db.session.execute(
                    text("CALL sp_editar_combo_detalle(:id_combo, :id_prod, :cant)"),
                    {
                        "id_combo": nuevo_id_combo,
                        "id_prod": det['id_prod'],
                        "cant": det['cant']
                    }
                )
                        
            db.session.commit()
            flash('Combo estructurado y guardado exitosamente.', 'success')
            return redirect(url_for('combos.principal'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error en combos (SP): {e}")
            flash('Error en base de datos. Verifica que el nombre no esté repetido.', 'error')
            return redirect(url_for('combos.principal'))
            
    else:
        flash('Corrige los campos marcados en rojo.', 'error')
        return redirect(url_for('combos.principal'))


@combos.route('/editar/<int:id_combo>', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente')
def editar(id_combo):
    form_edit = ComboForm(request.form) # Usamos form_edit

    if form_edit.validate():
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
                        detalles_a_guardar.append({
                            'id_prod': int(id_prod),
                            'cant': int(cant)
                        })
                        productos_validos += 1
                        
            if productos_validos < 2:
                flash('Error: Un combo debe contener al menos 2 productos válidos.', 'error')
                return redirect(url_for('combos.principal'))

            # Recuperamos la imagen actual consultando directamente
            combo_existente = db.session.execute(
                text("SELECT imagen FROM combos WHERE id_combo = :id"), 
                {"id": id_combo}
            ).fetchone()
            
            nombre_imagen = combo_existente[0] if combo_existente and combo_existente[0] else 'Combo.png'
            
            # ----- LÓGICA PARA ACTUALIZAR IMAGEN -----
            imagen_file = request.files.get('imagen')
            
            # Si subió archivo nuevo, reemplazamos la foto actual
            if imagen_file and imagen_file.filename != '':
                filename = secure_filename(imagen_file.filename)
                filepath = os.path.join(current_app.root_path, 'static', 'img', filename)
                imagen_file.save(filepath)
                nombre_imagen = filename
            # -----------------------------------------
            
            # 1. EJECUTAR SP PARA ACTUALIZAR INFO DEL COMBO
            db.session.execute(
                text("CALL sp_editar_combo_info(:id_combo, :nombre, :desc, :precio, :img)"),
                {
                    "id_combo": id_combo,
                    "nombre": form_edit.nombre.data,
                    "desc": form_edit.descripcion.data,
                    "precio": form_edit.precio_venta.data,
                    "img": nombre_imagen
                }
            )
            
            # 2. LIMPIAR DETALLES VIEJOS
            db.session.execute(
                text("DELETE FROM detalle_combos WHERE id_combo = :id"), 
                {"id": id_combo}
            )

            # 3. EJECUTAR SP PARA INSERTAR LOS NUEVOS DETALLES
            for det in detalles_a_guardar:
                db.session.execute(
                    text("CALL sp_editar_combo_detalle(:id_combo, :id_prod, :cant)"),
                    {
                        "id_combo": id_combo,
                        "id_prod": det['id_prod'],
                        "cant": det['cant']
                    }
                )

            db.session.commit()
            flash('Combo actualizado correctamente.', 'success')
            return redirect(url_for('combos.principal'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al editar combo (SP): {e}")
            flash('Hubo un error al actualizar el combo.', 'error')
            return redirect(url_for('combos.principal'))
    else:
        flash('Corrige los errores en rojo del combo.', 'error')
        return redirect(url_for('combos.principal'))