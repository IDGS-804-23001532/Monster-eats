from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models import db, InventarioProducto, Producto, Combo, MovimientoInventarioProducto
from datetime import datetime
from forms import AjusteStockForm, CrearComboForm, VincularComboForm

inventario_produccion = Blueprint('inventario_produccion', __name__, url_prefix='/inventario-produccion')

@inventario_produccion.route('/', methods=['GET', 'POST'])
def principal():
    form = AjusteStockForm() 
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESO DE AJUSTE ---")
        print("Datos recibidos:", request.form)
        
        if form.validate_on_submit():
            print("WTForms: Datos correctos.")
            id_prod = form.id_producto.data
            cantidad_ajuste = form.cantidad.data
            motivo = form.motivo.data
            
            try:
                inv = InventarioProducto.query.filter_by(id_producto=id_prod).first()
                
                if inv:
                    if inv.stock_actual + cantidad_ajuste < 0:
                        print("Error detectado: El stock quedaría en negativo.")
                        flash('No puedes restar más unidades de las que tienes disponibles.', 'error')
                        return redirect(url_for('inventario_produccion.principal'))

                    stock_anterior = inv.stock_actual
                    inv.stock_actual += cantidad_ajuste
                    
                    from models import Usuario
                    usuario_db = Usuario.query.first()
                    user_id = usuario_db.id_usuario if usuario_db else 1
                    
                    movimiento = MovimientoInventarioProducto(
                        id_producto=id_prod,
                        tipo_movimiento='AJUSTE_MANUAL',
                        cantidad=abs(cantidad_ajuste),
                        stock_anterior=stock_anterior,
                        stock_nuevo=inv.stock_actual,
                        motivo=motivo,
                        id_usuario=user_id, 
                        fecha_movimiento=datetime.now()
                    )
                    db.session.add(movimiento)
                    db.session.commit()
                    
                    print("ÉXITO: Ajuste guardado en la Base de Datos.")
                    flash('Cambio guardado de forma correcta.', 'success')
                    return redirect(url_for('inventario_produccion.principal'))
                else:
                     print("Error: Producto no encontrado.")
                     flash('No se encontro el producto.', 'error')
                     return redirect(url_for('inventario_produccion.principal'))
                     
            except Exception as e:
                db.session.rollback()
                print(f"CRÍTICO - ERROR DE BASE DE DATOS: {str(e)}")
                flash('Fallo al intentar guardar en BD.', 'error')
                return redirect(url_for('inventario_produccion.principal'))

        else:
            print("WTForms RECHAZÓ EL FORMULARIO. Errores:", form.errors)

    productos_stock = db.session.query(InventarioProducto, Producto)\
        .join(Producto, InventarioProducto.id_producto == Producto.id_producto)\
        .filter(~Producto.nombre.ilike('%combo%'))\
        .all()

    return render_template('inventario_Produccion/principal.html', 
                           productos_stock=productos_stock, 
                           form=form)

@inventario_produccion.route('/combos')
def combos_dinamicos():
    combos_padres = Producto.query.filter(Producto.nombre.ilike('%combo%'), Producto.activo == 1).all()

    combos_data = []
    for padre in combos_padres:
        hijos_info = db.session.query(Combo, Producto, InventarioProducto)\
            .join(Producto, Combo.id_producto_hijo == Producto.id_producto)\
            .outerjoin(InventarioProducto, Producto.id_producto == InventarioProducto.id_producto)\
            .filter(Combo.id_producto_padre == padre.id_producto)\
            .all()
        
        total_ingredientes = sum([hijo.Combo.cantidad for hijo in hijos_info])
        es_valido = total_ingredientes >= 2
        
        stock_combo_final = 0
        
        if es_valido:
            stock_posible = []
            for hijo in hijos_info:
                stock_actual = hijo.InventarioProducto.stock_actual if hijo.InventarioProducto else 0
                cantidad_requerida = hijo.Combo.cantidad
                stock_posible.append(int(stock_actual // cantidad_requerida))
                
            stock_combo_final = min(stock_posible) if stock_posible else 0

        combos_data.append({
            'padre': padre,
            'hijos': hijos_info,
            'stock_disponible': stock_combo_final,
            'es_valido': es_valido
        })

    return render_template('inventario_Produccion/combosDinamicos.html', combos_data=combos_data)

@inventario_produccion.route('/gestionar_combos', methods=['GET', 'POST'])
def gestionar_combos():
    form_crear = CrearComboForm()
    form_vincular = VincularComboForm()
    
    del form_vincular.id_padre

    # Llenamos las opciones del Paso 2
    posibles_ingredientes = Producto.query.filter(~Producto.nombre.ilike('%combo%'), Producto.activo==1).all()
    form_vincular.id_hijo.choices = [(0, 'Elige un producto...')] + [(p.id_producto, p.nombre) for p in posibles_ingredientes]

    # Preparamos la sesión
    if 'combo_temp' not in session:
        session['combo_temp'] = {'id_padre': None, 'nombre': '', 'precio': '', 'ingredientes': []}

    if request.method == 'POST':
        action = request.form.get('action')

        # ACCIÓN 1: FIJAR DATOS
        if action == 'guardar_datos_generales':
            if form_crear.validate_on_submit():
                session['combo_temp']['nombre'] = form_crear.nombre_combo.data
                session['combo_temp']['precio'] = float(form_crear.precio_combo.data)
                session.modified = True
                return redirect(url_for('inventario_produccion.gestionar_combos'))
            # Si falla la validación, el código sigue hacia abajo y pinta los errores en el HTML.

        # ACCIÓN 2: AÑADIR INGREDIENTE
        elif action == 'agregar_ingrediente':
            if form_vincular.validate_on_submit():
                id_hijo = form_vincular.id_hijo.data
                cantidad = form_vincular.cantidad.data
                
                if id_hijo == 0:
                    form_vincular.id_hijo.errors.append('Debes seleccionar un ingrediente de la lista.')
                else:
                    prod = Producto.query.get(id_hijo)
                    if prod:
                        combo_temp = session['combo_temp']
                        encontrado = False
                        for item in combo_temp['ingredientes']:
                            if item['id_producto'] == id_hijo:
                                item['cantidad'] += cantidad
                                encontrado = True
                                break
                        if not encontrado:
                            combo_temp['ingredientes'].append({'id_producto': id_hijo, 'nombre': prod.nombre, 'cantidad': cantidad})
                        session['combo_temp'] = combo_temp 
                        session.modified = True
                        return redirect(url_for('inventario_produccion.gestionar_combos'))
            # Si falla, sigue hacia abajo y pinta los errores en la caja de "Añadir".

        # ACCIÓN 3: FINALIZAR EL COMBO COMPLETO
        elif action == 'finalizar_combo':
            temp = session['combo_temp']
            nombre = temp.get('nombre')
            precio = temp.get('precio')
            ingredientes = temp.get('ingredientes', [])
            total_piezas = sum([i['cantidad'] for i in ingredientes])

            hay_errores = False

            # Validamos que se haya hecho el Paso 1 (AQUÍ ESTÁ LA CORRECCIÓN)
            if not nombre:
                form_crear.nombre_combo.errors = ['Falta fijar el nombre del paquete.']
                hay_errores = True
            if not precio:
                form_crear.precio_combo.errors = ['Falta fijar el precio.']
                hay_errores = True
                
            # Validamos que haya al menos 2 ingredientes
            if total_piezas < 2:
                flash('La receta debe contener al menos 2 productos físicos.', 'error_receta')
                hay_errores = True

            if not hay_errores:
                try:
                    nombre_final = f"Combo {nombre}" if "combo" not in nombre.lower() else nombre
                    if temp['id_padre']: 
                        nuevo_combo = Producto.query.get(temp['id_padre'])
                        nuevo_combo.nombre = nombre_final
                        nuevo_combo.precio_venta = precio
                        Combo.query.filter_by(id_producto_padre=temp['id_padre']).delete()
                    else: 
                        nuevo_combo = Producto(id_categoria=1, nombre=nombre_final, precio_venta=precio, activo=1)
                        db.session.add(nuevo_combo)
                        db.session.flush()
                        nuevo_inv = InventarioProducto(id_producto=nuevo_combo.id_producto, stock_actual=0)
                        db.session.add(nuevo_inv)

                    for item in ingredientes:
                        nueva_rel = Combo(id_producto_padre=nuevo_combo.id_producto, id_producto_hijo=item['id_producto'], cantidad=item['cantidad'])
                        db.session.add(nueva_rel)
                        
                    db.session.commit()
                    session.pop('combo_temp', None)
                    flash('Paquete guardado correctamente.', 'success')
                    return redirect(url_for('inventario_produccion.gestionar_combos'))
                except Exception as e:
                    db.session.rollback()
                    flash('Error en la base de datos.', 'error_receta')
            # Si hay errores, no hace redirect, solo renderiza la plantilla mostrando todas las alertas.

        # Cargar editar, activar/desactivar, eliminar y cancelar
        elif action == 'cargar_para_editar':
            id_padre = int(request.form.get('id_padre'))
            prod_padre = Producto.query.get(id_padre)
            relaciones = Combo.query.filter_by(id_producto_padre=id_padre).all()
            ingredientes_list = [{'id_producto': r.id_producto_hijo, 'nombre': Producto.query.get(r.id_producto_hijo).nombre, 'cantidad': r.cantidad} for r in relaciones]
            session['combo_temp'] = {'id_padre': id_padre, 'nombre': prod_padre.nombre.replace("Combo ", ""), 'precio': float(prod_padre.precio_venta), 'ingredientes': ingredientes_list}
            session.modified = True
            return redirect(url_for('inventario_produccion.gestionar_combos'))

        elif action == 'alternar_estado':
            id_prod = int(request.form.get('id_producto'))
            prod = Producto.query.get(id_prod)
            if prod:
                prod.activo = 0 if prod.activo == 1 else 1
                db.session.commit()
            return redirect(url_for('inventario_produccion.gestionar_combos'))

        elif action == 'eliminar_ingrediente':
            id_eliminar = int(request.form.get('id_eliminar'))
            session['combo_temp']['ingredientes'] = [i for i in session['combo_temp']['ingredientes'] if i['id_producto'] != id_eliminar]
            session.modified = True
            return redirect(url_for('inventario_produccion.gestionar_combos'))

        elif action == 'cancelar_combo':
            session.pop('combo_temp', None)
            return redirect(url_for('inventario_produccion.gestionar_combos'))

    # PREPARAR LA VISTA (Para GET o POST fallido)
    if request.method == 'GET' and session['combo_temp']['nombre']:
        form_crear.nombre_combo.data = session['combo_temp']['nombre']
        form_crear.precio_combo.data = session['combo_temp']['precio']

    combos_padres = Producto.query.filter(Producto.nombre.ilike('%combo%')).all()
    combos_data = []
    for padre in combos_padres:
        hijos = db.session.query(Combo, Producto).join(Producto, Combo.id_producto_hijo == Producto.id_producto).filter(Combo.id_producto_padre == padre.id_producto).all()
        combos_data.append({'padre': padre, 'hijos': hijos})

    return render_template('inventario_Produccion/gestionar_combos.html', 
                           combos_data=combos_data, 
                           form_crear=form_crear,
                           form_vincular=form_vincular,
                           ingredientes_disponibles=posibles_ingredientes,
                           combo_temp=session['combo_temp'])

@inventario_produccion.route('/eliminar_hijo_combo/<int:id_padre>/<int:id_hijo>', methods=['POST'])
def eliminar_hijo_combo(id_padre, id_hijo):
    try:
        Combo.query.filter_by(id_producto_padre=id_padre, id_producto_hijo=id_hijo).delete()
        db.session.commit()
        flash('Ingrediente quitado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Fallo al quitar.', 'error')
    return redirect(url_for('inventario_produccion.gestionar_combos'))