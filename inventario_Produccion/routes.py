from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models import db, Producto, Combo, InventarioProducto
from datetime import datetime
from forms import AjusteStockForm, CrearComboForm, VincularComboForm
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
from collections import namedtuple

inventario_produccion = Blueprint('inventario_produccion', __name__, url_prefix='/inventario-produccion')

# Creamos estructuras inmutables (Hashables) para engañar a WTForms y Jinja
InvMock = namedtuple('InvMock', ['stock_actual'])
ProdMock = namedtuple('ProdMock', ['id_producto', 'nombre', 'precio_venta'])

@inventario_produccion.route('/', methods=['GET', 'POST'])
@login_required
@roles_accepted('Cocina') # REGLA: Sólo el Cocina puede visualizar esto
def principal():
    form = AjusteStockForm() 
    
    if request.method == 'POST':
        if form.validate_on_submit():
            id_prod = form.id_producto.data
            cantidad_ajuste = form.cantidad.data
            motivo = form.motivo.data
            
            try:
                # Obtenemos el usuario autenticado actualmente
                user_id = current_user.id_usuario
                
                # Ejecutamos el Stored Procedure
                db.session.execute(
                    text("CALL sp_ajustar_stock_producto(:p_id, :p_cant, :p_motivo, :p_usr)"),
                    {'p_id': id_prod, 'p_cant': cantidad_ajuste, 'p_motivo': motivo, 'p_usr': user_id}
                )
                db.session.commit()
                flash('Cambio guardado de forma correcta.', 'success')
                
            except Exception as e:
                db.session.rollback()
                error_msg = str(e)
                # Manejamos el error específico del Stored Procedure
                if "Error_Stock_Negativo" in error_msg:
                    flash('No puedes restar más unidades de las que tienes disponibles.', 'error')
                else:
                    flash('Fallo al intentar guardar en BD.', 'error')
                    
            return redirect(url_for('inventario_produccion.principal'))

    productos_stock = []
    try:
        # Obtenemos los datos desde la Vista SQL de forma directa
        query = text("SELECT id_producto, nombre, precio_venta, stock_actual FROM vw_inventario_productos")
        # Usamos fetchall() directo para que devuelva tuplas puras en lugar de diccionarios
        resultados = db.session.execute(query).fetchall()
        
        for r in resultados:
            # Construimos nuestros objetos inmutables apuntando al índice (0=id, 1=nombre, 2=precio, 3=stock)
            inv = InvMock(stock_actual=r[3])
            prod = ProdMock(id_producto=r[0], nombre=r[1], precio_venta=r[2])
            productos_stock.append((inv, prod))
            
    except Exception as e:
        print(f"CRÍTICO EN GET: {e}")
        flash('Asegúrate de haber ejecutado las Vistas y SPs en la base de datos.', 'error')

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