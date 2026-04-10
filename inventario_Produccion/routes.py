from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Producto, InventarioProducto
from flask_security import login_required, roles_accepted, current_user
from forms import AjusteStockForm  
from audit_logger import audit  

inventario_produccion = Blueprint('inventario_produccion', __name__, url_prefix='/inventario-produccion')

@inventario_produccion.route('/', methods=['GET', 'POST'])
@login_required
<<<<<<< Updated upstream
@roles_accepted('Cocina') # REGLA: Sólo el Cocina puede visualizar esto
=======
@roles_accepted('administrador', 'gerente', 'cocina', 'cocinero')
>>>>>>> Stashed changes
def principal():
    # Instanciamos el formulario de Flask-WTF
    form = AjusteStockForm()

    # ---------------------------------------------------------
    # LÓGICA POST: Si el usuario envió el formulario del modal
    # ---------------------------------------------------------
    if form.validate_on_submit():
        try:
            id_prod = form.id_producto.data
            cantidad_ajuste = form.cantidad.data  # Puede ser positivo (+5) o negativo (-2)
            motivo = form.motivo.data

            # Buscamos el registro de inventario actual
            inventario = InventarioProducto.query.filter_by(id_producto=id_prod).first()
            
            # Si no existía un registro previo, lo creamos desde cero
            if not inventario:
                inventario = InventarioProducto(id_producto=id_prod, stock_actual=0)
                db.session.add(inventario)
            
            # Aplicamos la suma algebraica (si ingresó -5, se restará. Si ingresó 10, se sumará)
            inventario.stock_actual += cantidad_ajuste

            db.session.commit()

            # Guardamos el movimiento en la bitácora de auditoría (MongoDB)
            audit.log_action(
                module_name="inventario_produccion", 
                action="Ajuste Manual de Stock", 
                details={
                    "id_producto": id_prod, 
                    "ajuste": cantidad_ajuste, 
                    "stock_resultante": inventario.stock_actual,
                    "motivo": motivo
                },
                level="INFO"
            )

            flash('¡Stock ajustado correctamente!', 'success')
            return redirect(url_for('inventario_produccion.principal'))

        except Exception as e:
            db.session.rollback()
            print(f"Error al ajustar stock en producción: {e}")
            flash('Error en la base de datos al guardar el ajuste.', 'error')
            
    elif request.method == 'POST':
        # Si el form se envió pero no pasó las validaciones de WTF
        flash('Error en los datos ingresados. Revisa el formulario.', 'error')

<<<<<<< Updated upstream
    return render_template('inventario_Produccion/principal.html', 
                           productos_stock=productos_stock, 
                           form=form)

@inventario_produccion.route('/combos')
@login_required
@roles_accepted('Cocina')
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
@login_required
@roles_accepted('Cocina')
def gestionar_combos():
    form_crear = CrearComboForm()
    form_vincular = VincularComboForm()
    
    del form_vincular.id_padre

    # Llenamos las opciones del Paso 2
    posibles_ingredientes = Producto.query.filter(~Producto.nombre.ilike('%combo%'), Producto.activo==1).all()
    form_vincular.id_hijo.choices = [(0, 'Elige un producto...')] + [(p.id_producto, p.nombre) for p in posibles_ingredientes]

    if 'combo_temp' not in session:
        session['combo_temp'] = {'id_padre': None, 'nombre': '', 'precio': '', 'ingredientes': []}

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'guardar_datos_generales':
            if form_crear.validate_on_submit():
                session['combo_temp']['nombre'] = form_crear.nombre_combo.data
                session['combo_temp']['precio'] = float(form_crear.precio_combo.data)
                session.modified = True
                return redirect(url_for('inventario_produccion.gestionar_combos'))

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

        elif action == 'finalizar_combo':
            temp = session['combo_temp']
            nombre = temp.get('nombre')
            precio = temp.get('precio')
            ingredientes = temp.get('ingredientes', [])
            total_piezas = sum([i['cantidad'] for i in ingredientes])

            hay_errores = False

            if not nombre:
                form_crear.nombre_combo.errors = ['Falta fijar el nombre del paquete.']
                hay_errores = True
            if not precio:
                form_crear.precio_combo.errors = ['Falta fijar el precio.']
                hay_errores = True
                
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

                    # REGISTRO DE AUDITORÍA: Creación/Modificación de Receta
                    audit.log_action(
                        module_name="logs_inventario", # <--- ¡AQUÍ ESTÁ EL CAMBIO!
                        action="Modificación de Combo/Receta", 
                        details={
                            "nombre_combo": nombre_final, 
                            "precio_asignado": precio,
                            "piezas_totales": total_piezas
                        }, 
                        level="WARNING"
                    )
                    
                    flash('Paquete guardado correctamente.', 'success')
                    return redirect(url_for('inventario_produccion.gestionar_combos'))
                except Exception as e:
                    db.session.rollback()
                    flash('Error en la base de datos.', 'error_receta')

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
@login_required
@roles_accepted('Cocina')
def eliminar_hijo_combo(id_padre, id_hijo):
    try:
        Combo.query.filter_by(id_producto_padre=id_padre, id_producto_hijo=id_hijo).delete()
        db.session.commit()
        flash('Ingrediente quitado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Fallo al quitar.', 'error')
    return redirect(url_for('inventario_produccion.gestionar_combos'))
=======
    # 1. Filtramos inteligentemente: Solo productos activos que NO son combos y NO se hacen al momento
    productos_lote = Producto.query.filter_by(
        activo=True, 
    ).all()
    
    # 2. Armamos las parejas (tuplas) que tu HTML necesita
    productos_stock = []
    for prod in productos_lote:
        inv = InventarioProducto.query.filter_by(id_producto=prod.id_producto).first()
        
        # Si el producto es nuevo y aún no tiene registro de stock, creamos un objeto temporal en 0
        # (Nota: No lo guardamos en la base de datos aún, solo es para que el HTML pueda pintarlo sin errores)
        if not inv:
            inv = InventarioProducto(id_producto=prod.id_producto, stock_actual=0)
            
        # Agregamos la pareja exacta (inv, prod) a la lista
        productos_stock.append((inv, prod))
    
    # Mandamos los datos al HTML, incluyendo el formulario para los modales
    return render_template(
        'inventario_Produccion/principal.html', 
        productos_stock=productos_stock, 
        form=form
    )
>>>>>>> Stashed changes
