from flask import render_template, request, abort, session, redirect, url_for, flash, jsonify, current_app
from sqlalchemy.exc import OperationalError, DBAPIError
from Pagina import pagina_bp
from models import db, Producto, CategoriaProducto, Combo, Receta, Insumo, UnidadMedida, MetodoPago, InventarioProducto, LoteInsumo
from flask_security import login_required, current_user

# ── Helpers ─────────────────────────────────────────────────────────────────

def _get_ingredientes(id_producto):
    """Devuelve lista de dicts {nombre, cantidad, unidad} para un producto."""
    rows = (
        db.session.query(
            Insumo.nombre.label('nombre'),
            Receta.cantidad_requerida.label('cantidad'),
            UnidadMedida.abreviatura.label('unidad'),
        )
        .join(Receta, Receta.id_insumo == Insumo.id_insumo)
        .join(UnidadMedida, Insumo.id_unidad_medida == UnidadMedida.id_unidad_medida)
        .filter(Receta.id_producto == id_producto)
        .all()
    )
    return [{'nombre': r.nombre, 'cantidad': float(r.cantidad), 'unidad': r.unidad} for r in rows]


def _tiene_ingredientes_suficientes(id_producto):
    """Verifica si hay suficientes insumos en lotes para producir 1 unidad del producto."""
    receta_rows = Receta.query.filter_by(id_producto=id_producto).all()
    # Si no tiene receta definida asumimos que no se produce (depende solo del inventario de producto)
    if not receta_rows:
        return False

    for r in receta_rows:
        # Sumar cantidad disponible en lotes para el insumo
        stock = db.session.query(db.func.coalesce(db.func.sum(LoteInsumo.cantidad_disponible), 0)).filter(
            LoteInsumo.id_insumo == r.id_insumo,
            LoteInsumo.cantidad_disponible > 0
        ).scalar() or 0

        # comparar con la cantidad requerida para 1 unidad
        try:
            req = float(r.cantidad_requerida)
        except Exception:
            req = float(r.cantidad_requerida or 0)

        if stock < req:
            return False

    return True


# ── Menú por categoría ───────────────────────────────────────────────────────

@pagina_bp.route('/menu/<categoria>', methods=['GET'])
def menu_categoria(categoria):
    q = request.args.get('q', '').strip()

    if categoria.lower() == 'combos':
        nombre_cat = 'Combos'
        combos_qs = Combo.query.filter_by(activo=True)
        if q:
            combos_qs = combos_qs.filter(Combo.nombre.ilike(f"%{q}%"))

        productos = []
        for c in combos_qs.all():
            # Determinar disponibilidad del combo: todos los productos con stock suficiente
            disponible = True
            for det in c.detalles:
                inv = InventarioProducto.query.filter_by(id_producto=det.id_producto).first()
                stock = inv.stock_actual if inv else 0
                if stock < det.cantidad:
                    disponible = False
                    break

            productos.append({
                'nombre':       c.nombre,
                'precio_venta': c.precio_venta,
                'imagen':       c.imagen or 'default_combo.png',
                'es_combo':     True,
                'id_combo':     c.id_combo,
                'id_producto':  None,
                'disponible':   disponible,
            })

        return render_template(
            'Pagina/Productos.html',
            productos=productos,
            categoria_nombre=nombre_cat,
            categoria_param=categoria,
            q=q
        )

    cat = CategoriaProducto.query.filter(CategoriaProducto.nombre.ilike(categoria)).first()

    if not cat:
        productos = []
        nombre_cat = categoria.capitalize()
    else:
        nombre_cat = cat.nombre
        # Obtener productos como diccionarios con disponibilidad
        qs = Producto.query.filter_by(id_categoria=cat.id_categoria, activo=True)
        if q:
            qs = qs.filter(Producto.nombre.ilike(f"%{q}%"))

        productos = []
        for p in qs.all():
            inv = InventarioProducto.query.filter_by(id_producto=p.id_producto).first()
            stock = inv.stock_actual if inv else 0
            # Disponible si hay producto en inventario o si hay insumos suficientes para producirlo
            puede_producir = _tiene_ingredientes_suficientes(p.id_producto)
            productos.append({
                'nombre':       p.nombre,
                'precio_venta': p.precio_venta,
                'imagen':       p.imagen or 'default_product.png',
                'es_combo':     False,
                'id_combo':     None,
                'id_producto':  p.id_producto,
                'disponible':   True if stock > 0 or puede_producir else False,
                'stock':        int(stock),
                'puede_producir': puede_producir,
            })

    return render_template(
        'Pagina/Productos.html',
        productos=productos,
        categoria_nombre=nombre_cat,
        categoria_param=categoria,
        q=q
    )


@pagina_bp.route('/buscar', methods=['GET'])
def buscar():
    """Buscador global que busca en productos y combos por nombre.
    Devuelve la misma plantilla de catálogo con resultados combinados.
    """
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('pagina.menu_categoria', categoria='Hamburguesas'))

    productos = []

    # Buscar productos
    prods = Producto.query.filter(Producto.nombre.ilike(f"%{q}%"), Producto.activo == True)
    for p in prods.all():
        inv = InventarioProducto.query.filter_by(id_producto=p.id_producto).first()
        stock = inv.stock_actual if inv else 0
        puede_producir = _tiene_ingredientes_suficientes(p.id_producto)
        productos.append({
            'nombre':       p.nombre,
            'precio_venta': p.precio_venta,
            'imagen':       p.imagen or 'default_product.png',
            'es_combo':     False,
            'id_combo':     None,
            'id_producto':  p.id_producto,
            'disponible':   True if stock > 0 or puede_producir else False,
            'stock':        int(stock),
            'puede_producir': puede_producir,
        })

    # Buscar combos
    combos_qs = Combo.query.filter(Combo.nombre.ilike(f"%{q}%"), Combo.activo == True).all()
    for c in combos_qs:
        disponible = True
        for det in c.detalles:
            inv = InventarioProducto.query.filter_by(id_producto=det.id_producto).first()
            stock = inv.stock_actual if inv else 0
            if stock < det.cantidad:
                disponible = False
                break
        productos.append({
            'nombre':       c.nombre,
            'precio_venta': c.precio_venta,
            'imagen':       c.imagen or 'default_combo.png',
            'es_combo':     True,
            'id_combo':     c.id_combo,
            'id_producto':  None,
            'disponible':   disponible,
        })

    categoria_nombre = f'Resultados para "{q}"'
    return render_template('Pagina/Productos.html', productos=productos, categoria_nombre=categoria_nombre, categoria_param='buscar', q=q)


# ── Detalle de Producto ──────────────────────────────────────────────────────

@pagina_bp.route('/producto/<int:id_producto>', methods=['GET'])
def producto_detalle(id_producto):
    producto = Producto.query.filter_by(id_producto=id_producto, activo=True).first_or_404()
    categoria = CategoriaProducto.query.get(producto.id_categoria)
    ingredientes = _get_ingredientes(id_producto)

    # Verificar stock del producto terminado
    inv = InventarioProducto.query.filter_by(id_producto=id_producto).first()
    stock = inv.stock_actual if inv else 0
    # Si no hay producto en inventario, pero sí se pueden producir insumos, permitirlo
    if stock <= 0 and not _tiene_ingredientes_suficientes(id_producto):
        # Mostrar la misma plantilla pero indicando que está fuera de stock (no acceso completo)
        return render_template(
            'Pagina/descripcion.html',
            producto=producto,
            categoria=categoria,
            ingredientes=ingredientes,
            es_combo=False,
            out_of_stock=True,
            next=url_for('pagina.menu_categoria', categoria=categoria.nombre if categoria else 'Hamburguesas')
        )

    return render_template(
        'Pagina/descripcion.html',
        producto=producto,
        categoria=categoria,
        ingredientes=ingredientes,
        es_combo=False,
    )


# ── Detalle de Combo ─────────────────────────────────────────────────────────

@pagina_bp.route('/combo/<int:id_combo>', methods=['GET'])
def combo_detalle(id_combo):
    combo = Combo.query.filter_by(id_combo=id_combo, activo=True).first_or_404()
    detalles = []
    disponible = True
    for det in combo.detalles:
        detalles.append({
            'producto':     det.producto,
            'cantidad':     det.cantidad,
            'ingredientes': _get_ingredientes(det.id_producto),
        })
        inv = InventarioProducto.query.filter_by(id_producto=det.id_producto).first()
        stock = inv.stock_actual if inv else 0
        # Considerar tanto inventario de producto terminado como posibilidad de producirlo
        puede_producir = _tiene_ingredientes_suficientes(det.id_producto)
        if stock < det.cantidad and not puede_producir:
            disponible = False

    if not disponible:
        return render_template(
            'Pagina/descripcion.html',
            combo=combo,
            detalles=detalles,
            es_combo=True,
            out_of_stock=True,
            next=url_for('pagina.menu_categoria', categoria='Combos')
        )

    return render_template(
        'Pagina/descripcion.html',
        combo=combo,
        detalles=detalles,
        es_combo=True,
    )


# ── Carrito (sesión) ─────────────────────────────────────────────────────────

def _get_carrito():
    """Obtiene la lista de items del carrito desde la sesión."""
    return session.get('carrito', [])

def _save_carrito(carrito):
    """Guarda la lista de items del carrito en la sesión."""
    session['carrito'] = carrito


@pagina_bp.route('/carrito/validar_agregar', methods=['POST'])
def carrito_validar_agregar():
    """Valida si el usuario está logueado antes de agregar.
    Si está logueado delega en `carrito_agregar()`. Si no, muestra una card
    que pide iniciar sesión (sin usar el carrito como destino).
    """
    # Si está autenticado, reusar la lógica existente (llama a la función)
    if current_user.is_authenticated:
        return carrito_agregar()

    # No autenticado: renderizar una card indicando que debe iniciar sesión.
    # Determinar si el formulario incluye id_producto o id_combo y renderizar
    # la página de descripción con la card inline (sin navegar al panel ERP).
    id_producto = request.form.get('id_producto', type=int)
    id_combo = request.form.get('id_combo', type=int)

    # Si tenemos id_producto -> renderizar detalle de producto con card
    if id_producto:
        producto = Producto.query.filter_by(id_producto=id_producto, activo=True).first_or_404()
        categoria = CategoriaProducto.query.get(producto.id_categoria)
        ingredientes = _get_ingredientes(id_producto)
        return render_template(
            'Pagina/descripcion.html',
            producto=producto,
            categoria=categoria,
            ingredientes=ingredientes,
            es_combo=False,
            show_login_card=True,
            next=url_for('pagina.producto_detalle', id_producto=id_producto)
        )

    # Si tenemos id_combo -> renderizar detalle de combo con card
    if id_combo:
        combo = Combo.query.filter_by(id_combo=id_combo, activo=True).first_or_404()
        detalles = []
        for det in combo.detalles:
            detalles.append({
                'producto':     det.producto,
                'cantidad':     det.cantidad,
                'ingredientes': _get_ingredientes(det.id_producto),
            })
        return render_template(
            'Pagina/descripcion.html',
            combo=combo,
            detalles=detalles,
            es_combo=True,
            show_login_card=True,
            next=url_for('pagina.combo_detalle', id_combo=id_combo)
        )

    # Fallback: si no hay ids, mostrar la card simple
    target = request.referrer or url_for('pagina.menu_categoria', categoria='Hamburguesas')
    return render_template('Pagina/login_card.html', next=target)


@pagina_bp.route('/carrito/agregar', methods=['POST'])
def carrito_agregar():
    """Agrega un producto o combo al carrito desde la página de descripción."""
    id_producto = request.form.get('id_producto', type=int)
    id_combo    = request.form.get('id_combo', type=int)
    cantidad    = request.form.get('cantidad', 1, type=int)

    # Si no está autenticado, redirigir al detalle con ?show_login=1 (sin JS) o devolver JSON para AJAX
    if not current_user.is_authenticated:
        # Construir URL de destino: si existe referrer, usarlo (soporta listas),
        # si no, usar la página de detalle correspondiente.
        if request.referrer:
            target = request.referrer
        elif id_combo:
            target = url_for('pagina.combo_detalle', id_combo=id_combo)
        elif id_producto:
            target = url_for('pagina.producto_detalle', id_producto=id_producto)
        else:
            target = url_for('pagina.menu_categoria', categoria='Hamburguesas')

        # Mantener compatibilidad con peticiones AJAX (XHR)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'login_required': True, 'login_url': url_for('auth.login')})

        # Añadir query param show_login=1
        from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
        p = urlparse(target)
        qs = dict(parse_qsl(p.query))
        qs['show_login'] = '1'
        new_q = urlencode(qs)
        target = urlunparse((p.scheme, p.netloc, p.path, p.params, new_q, p.fragment))
        return redirect(target)

    carrito = _get_carrito()

    if id_combo:
        combo = Combo.query.get_or_404(id_combo)
        key = f'combo_{id_combo}'
        # Buscar si ya existe en el carrito
        for item in carrito:
            if item['key'] == key:
                item['cantidad'] += cantidad
                _save_carrito(carrito)
                msg = f'{combo.nombre} actualizado en tu pedido.'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': True, 'message': msg, 'redirect': request.referrer or url_for('pagina.menu_categoria', categoria='Combos')})
                flash(msg, 'success')
                return redirect(request.referrer or url_for('pagina.menu_categoria', categoria='Combos'))

        carrito.append({
            'key':       key,
            'es_combo':  True,
            'id':        id_combo,
            'nombre':    combo.nombre,
            'precio':    float(combo.precio_venta),
            'imagen':    combo.imagen,
            'carpeta':   '',
            'cantidad':  cantidad,
        })
    elif id_producto:
        producto = Producto.query.get_or_404(id_producto)
        cat = CategoriaProducto.query.get(producto.id_categoria)
        key = f'prod_{id_producto}'
        for item in carrito:
            if item['key'] == key:
                item['cantidad'] += cantidad
                _save_carrito(carrito)
                msg = f'{producto.nombre} actualizado en tu pedido.'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': True, 'message': msg, 'redirect': request.referrer or url_for('pagina.menu_categoria', categoria=cat.nombre if cat else 'Hamburguesas')})
                flash(msg, 'success')
                return redirect(request.referrer or url_for('pagina.menu_categoria', categoria=cat.nombre if cat else 'Hamburguesas'))

        carrito.append({
            'key':       key,
            'es_combo':  False,
            'id':        id_producto,
            'nombre':    producto.nombre,
            'precio':    float(producto.precio_venta),
            'imagen':    producto.imagen,
            'carpeta':   'productos',
            'cantidad':  cantidad,
        })
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Producto no encontrado.'}), 404
        flash('Producto no encontrado.', 'error')
        return redirect(request.referrer or '/')

    _save_carrito(carrito)
    msg = 'Producto añadido a tu pedido.'
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': msg, 'redirect': request.referrer or '/'})
    flash(msg, 'success')
    return redirect(request.referrer or '/')

# Otras rutas relacionadas con el carrito y pagos se encuentran al final de este archivo.
@pagina_bp.route('/carrito/action', methods=['POST'])
@login_required # Opcional, dependiendo de si permites ver el carrito sin login
def carrito_action():
    """Maneja las acciones del carrito: +1, -1, eliminar, vaciar y CONFIRMAR COMPRA."""
    accion = request.form.get('accion')
    item_key = request.form.get('item_key')
    current_app.logger.info('carrito_action entry: accion=%s item_key=%s form=%s', accion, item_key, dict(request.form))
    
    # Si no está autenticado y trata de hacer algo, redirigir
    if not current_user.is_authenticated:
        return render_template('Pagina/login_required.html', next=request.path)

    id_usuario = current_user.id_usuario
    carrito = _get_carrito()
    current_app.logger.info('carrito_action usuario=%s carrito=%s', id_usuario, carrito)

    # --- ACCIONES BÁSICAS ---
    if accion == 'agregar' and item_key:
        for item in carrito:
            if item['key'] == item_key:
                item['cantidad'] += 1
                break
        _save_carrito(carrito)

    elif accion == 'quitar_unidad' and item_key:
        for item in carrito:
            if item['key'] == item_key:
                item['cantidad'] -= 1
                if item['cantidad'] <= 0:
                    carrito.remove(item)
                break
        _save_carrito(carrito)

    elif accion == 'eliminar' and item_key:
        carrito = [i for i in carrito if i['key'] != item_key]
        _save_carrito(carrito)

    elif accion == 'vaciar':
        _save_carrito([])
        flash('Carrito vaciado.', 'info')

    # --- LÓGICA DE CONFIRMACIÓN (SIMILAR A VENTAS.PY) ---
    elif accion == 'confirmar':
        numero_cuenta = request.form.get('numero_cuenta', '').strip()
        current_app.logger.info('confirmar: numero_cuenta=%s', '***present***' if numero_cuenta else '***empty***')
        
        if not carrito:
            flash('Tu carrito está vacío.', 'error')
            return redirect(url_for('pagina.carrito_ver'))
        
        if not numero_cuenta or len(numero_cuenta) < 16:
            flash('Ingresa un número de tarjeta válido.', 'error')
            return redirect(url_for('pagina.carrito_ver'))

        # Buscamos el ID del método 'Tarjeta'
        metodo_tarjeta = MetodoPago.query.filter(MetodoPago.nombre.ilike('tarjeta')).first()
        if not metodo_tarjeta:
            flash('Error: El método de pago Tarjeta no está configurado en el sistema.', 'error')
            return redirect(url_for('pagina.carrito_ver'))

        # Conexión directa para manejar los resultsets del SP
        connection = db.engine.raw_connection()
        cursor = connection.cursor()

        try:
            # 1. Sincronizar Carrito de Sesión a la BD
            # Primero limpiamos lo que el usuario pueda tener en la tabla carrito
            current_app.logger.info('confirmar: sincronizando carrito a BD para usuario=%s', id_usuario)
            # Eliminar cualquier borrador previo en ventas_borrador para este usuario
            try:
                vb = db.session.execute(
                    db.text("SELECT id_venta_borrador FROM ventas_borrador WHERE id_usuario = :uid AND estado = 'ABIERTA' LIMIT 1"),
                    {'uid': id_usuario}
                ).mappings().first()
                if vb and vb.get('id_venta_borrador'):
                    id_vb_prev = vb.get('id_venta_borrador')
                    current_app.logger.info('Eliminar borrador previo id_venta_borrador=%s para usuario=%s', id_vb_prev, id_usuario)
                    db.session.execute(db.text("DELETE FROM detalle_ventas_borrador WHERE id_venta_borrador = :vb"), {'vb': id_vb_prev})
                    db.session.execute(db.text("DELETE FROM ventas_borrador WHERE id_venta_borrador = :vb"), {'vb': id_vb_prev})
                    db.session.commit()
            except Exception:
                db.session.rollback()
                current_app.logger.exception('Error eliminando borrador previo para usuario %s', id_usuario)
            
            # Insertamos los items directamente en ventas_borrador y detalle_ventas_borrador
            # Crear un nuevo borrador para el usuario
            try:
                db.session.execute(
                    db.text("INSERT INTO ventas_borrador (id_usuario, descuento_global, estado) VALUES (:uid, 0.00, 'ABIERTA')"),
                    {'uid': id_usuario}
                )
                db.session.commit()
            except Exception as ie:
                db.session.rollback()
                current_app.logger.exception('Error insertando ventas_borrador: %s', ie)
                raise

            # Obtener el borrador recien creado consultando por usuario y fecha
            try:
                vb_row = db.session.execute(
                    db.text("SELECT id_venta_borrador FROM ventas_borrador WHERE id_usuario = :uid AND estado = 'ABIERTA' ORDER BY fecha_creacion DESC LIMIT 1"),
                    {'uid': id_usuario}
                ).mappings().first()
                id_vb = vb_row['id_venta_borrador'] if vb_row else None
            except Exception as le:
                current_app.logger.exception('No se pudo obtener id del borrador por consulta: %s', le)
                id_vb = None

            if not id_vb:
                current_app.logger.error('No se pudo crear ventas_borrador (id_vb es None) para usuario=%s', id_usuario)
                raise Exception('No se pudo crear ventas_borrador')

            current_app.logger.info('confirmar: creado ventas_borrador id=%s para usuario=%s', id_vb, id_usuario)

            for item in carrito:
                cant = int(item.get('cantidad', 1))
                if item.get('es_combo'):
                    id_combo = int(item.get('id'))
                    combo = Combo.query.get(id_combo)
                    if not combo:
                        raise Exception(f'Combo no encontrado: {id_combo}')
                    precio = float(combo.precio_venta)
                    db.session.execute(
                        db.text("INSERT INTO detalle_ventas_borrador (id_venta_borrador, id_combo, cantidad, precio_unitario) VALUES (:vb, :id_combo, :cant, :precio)"),
                        {'vb': id_vb, 'id_combo': id_combo, 'cant': cant, 'precio': precio}
                    )
                    current_app.logger.info('confirmar: insert detalle_borrador combo=%s cantidad=%s', id_combo, cant)
                else:
                    id_prod = int(item.get('id'))
                    producto = Producto.query.get(id_prod)
                    if not producto:
                        raise Exception(f'Producto no encontrado: {id_prod}')
                    precio = float(producto.precio_venta)
                    db.session.execute(
                        db.text("INSERT INTO detalle_ventas_borrador (id_venta_borrador, id_producto, cantidad, precio_unitario) VALUES (:vb, :id_prod, :cant, :precio)"),
                        {'vb': id_vb, 'id_prod': id_prod, 'cant': cant, 'precio': precio}
                    )
                    current_app.logger.info('confirmar: insert detalle_borrador producto=%s cantidad=%s', id_prod, cant)

            db.session.commit()

            # 2. Ejecutar sp_venta_completar
            id_metodo = metodo_tarjeta.id_metodo_pago
            monto_recibido = 0.00 # En tarjeta no se calcula cambio usualmente

            current_app.logger.info('confirmar: llamando sp_venta_completar usuario=%s metodo=%s', id_usuario, id_metodo)
            cursor.callproc('sp_venta_completar', (id_usuario, id_metodo, numero_cuenta, monto_recibido))
            
            id_venta = None
            # Capturar el ID de venta (manejo de resultados según el driver)
            if hasattr(cursor, 'stored_results'):
                for result_set in cursor.stored_results():
                    row = result_set.fetchone()
                    if row: id_venta = row[0]
            else:
                row = cursor.fetchone()
                if row: id_venta = row[0]
                while cursor.nextset(): pass # Consumir otros sets

            connection.commit()
            
            # 3. Finalizar sesión
            # Asegurar que exista un ticket para esta venta (algunos entornos no lo crean en el SP)
            try:
                t = db.session.execute(db.text("SELECT id_ticket FROM tickets WHERE id_venta = :idv LIMIT 1"), {'idv': id_venta}).mappings().first()
                if not t:
                    # Obtener el total de la venta para monto_pagado
                    total_row = db.session.execute(db.text("SELECT total FROM ventas WHERE id_venta = :idv LIMIT 1"), {'idv': id_venta}).mappings().first()
                    monto_pagado = float(total_row['total']) if total_row and total_row.get('total') is not None else 0.00
                    folio = db.session.execute(db.text("SELECT CONCAT('TKT-', LPAD(:idv, 8, '0')) AS folio"), {'idv': id_venta}).scalar()
                    db.session.execute(db.text("INSERT INTO tickets (id_venta, folio, monto_pagado) VALUES (:idv, :folio, :monto)"), {'idv': id_venta, 'folio': folio, 'monto': monto_pagado})
                    db.session.commit()
                    current_app.logger.info('Ticket creado manualmente id_venta=%s folio=%s monto=%s', id_venta, folio, monto_pagado)
            except Exception:
                db.session.rollback()
                current_app.logger.exception('Error asegurando ticket para venta %s', id_venta)

            _save_carrito([]) # Limpiar carrito de sesión
            session['ticket_a_imprimir'] = id_venta
            flash('¡Compra realizada con éxito! Tu pedido está en cocina.', 'success')
            
            return redirect(url_for('pagina.carrito_ver'))

        except (OperationalError, DBAPIError, Exception) as e:
            connection.rollback()
            db.session.rollback()
            current_app.logger.exception('Error en confirmar/venta: %s', e)
            mensaje_usuario = 'Error al procesar la compra'
            # Extraer mensaje de SIGNAL 45000 de MySQL
            try:
                if hasattr(e, 'orig') and getattr(e.orig, 'args', None):
                    codigo_mysql = e.orig.args[0]
                    mensaje_mysql = e.orig.args[1] if len(e.orig.args) > 1 else str(e.orig)
                    if codigo_mysql == 1644:
                        mensaje_usuario = mensaje_mysql
                    else:
                        mensaje_usuario = mensaje_mysql
                else:
                    mensaje_usuario = str(e)
            except Exception:
                mensaje_usuario = str(e)

            flash(mensaje_usuario, 'error')
            return redirect(url_for('pagina.carrito_ver'))
            
        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('pagina.carrito_ver'))

# Rutas relacionadas con el KDS (tablero de cocina) se encuentran en el archivo `tablero_kds/routes.py` para mantener la separación de responsabilidades.
@pagina_bp.route('/carrito', methods=['GET'])
def carrito_ver():
    """Muestra la página del carrito."""
    # Si no está autenticado, mostrar la card de login inline en la vista del carrito
    if not current_user.is_authenticated:
        # Renderizar la misma plantilla de carrito pero pidiendo credenciales
        ticket_a_imprimir = session.pop('ticket_a_imprimir', None)
        return render_template('Pagina/comprar.html', carrito=[], total=0.0, total_items=0, show_login_card=True, next=request.path, ticket_a_imprimir=ticket_a_imprimir)

    carrito = _get_carrito()

    # Calcular subtotales
    for item in carrito:
        item['subtotal'] = item['precio'] * item['cantidad']

    total = sum(i['subtotal'] for i in carrito)
    total_items = sum(i['cantidad'] for i in carrito)

    return render_template(
        'Pagina/comprar.html',
        carrito=carrito,
        total=total,
        total_items=total_items,
        ticket_a_imprimir=session.pop('ticket_a_imprimir', None),
    )


@pagina_bp.route('/pago/online', methods=['POST'])
def pago_online():
    """Procesa un pago en línea desde el sitio público.
    Llama al stored procedure `sp_venta_completar` como en la vista de caja.
    """
    # Requerimos sesión: si no está autenticado, mostramos la card de login
    if not current_user.is_authenticated:
        return render_template('Pagina/login_card.html', next=request.referrer or url_for('pagina.carrito_ver'))

    # Obtener datos del formulario
    id_usuario = current_user.id_usuario
    id_metodo = request.form.get('metodo_pago', type=int)
    num_cuenta = request.form.get('numero_cuenta') or None
    monto_recibido = request.form.get('monto_recibido', 0.0, type=float)

    # Si no envían método, intentar usar 'tarjeta' por defecto
    if not id_metodo:
        metodo_tarjeta = MetodoPago.query.filter(MetodoPago.nombre.ilike('tarjeta')).first()
        id_metodo = metodo_tarjeta.id_metodo_pago if metodo_tarjeta else None

    try:
        # Asegurar que el carrito en BD corresponde al carrito en sesión
        carrito_sesion = _get_carrito()
        if not carrito_sesion:
            flash('Tu carrito está vacío. Agrega productos antes de pagar.', 'error')
            return redirect(url_for('pagina.carrito_ver'))

        # 1) Limpiar carrito en BD para el usuario autenticado
        current_app.logger.info('Iniciando limpieza/transferencia de carrito para usuario %s', id_usuario)
        current_app.logger.info('Carrito de sesión antes de transferir: %s', carrito_sesion)
        # Eliminar borrador previo si existe
        try:
            vb = db.session.execute(
                db.text("SELECT id_venta_borrador FROM ventas_borrador WHERE id_usuario = :uid AND estado = 'ABIERTA' LIMIT 1"),
                {'uid': id_usuario}
            ).mappings().first()
            if vb and vb.get('id_venta_borrador'):
                id_vb_prev = vb.get('id_venta_borrador')
                current_app.logger.info('Eliminar borrador previo id_venta_borrador=%s para usuario=%s', id_vb_prev, id_usuario)
                db.session.execute(db.text("DELETE FROM detalle_ventas_borrador WHERE id_venta_borrador = :vb"), {'vb': id_vb_prev})
                db.session.execute(db.text("DELETE FROM ventas_borrador WHERE id_venta_borrador = :vb"), {'vb': id_vb_prev})
                db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Error eliminando borrador previo antes de transferir carrito para usuario %s', id_usuario)

        # 2) Transferir items del carrito de sesión a ventas_borrador / detalle_ventas_borrador
        # Crear un nuevo borrador
        try:
            db.session.execute(
                db.text("INSERT INTO ventas_borrador (id_usuario, descuento_global, estado) VALUES (:uid, 0.00, 'ABIERTA')"),
                {'uid': id_usuario}
            )
            db.session.commit()
        except Exception as ie:
            db.session.rollback()
            current_app.logger.exception('Error insertando ventas_borrador (pago_online): %s', ie)
            raise

        try:
            vb_row = db.session.execute(
                db.text("SELECT id_venta_borrador FROM ventas_borrador WHERE id_usuario = :uid AND estado = 'ABIERTA' ORDER BY fecha_creacion DESC LIMIT 1"),
                {'uid': id_usuario}
            ).mappings().first()
            id_vb = vb_row['id_venta_borrador'] if vb_row else None
        except Exception as le:
            current_app.logger.exception('No se pudo obtener id del borrador (pago_online) por consulta: %s', le)
            id_vb = None

        if not id_vb:
            current_app.logger.error('No se pudo crear ventas_borrador (pago_online) para usuario=%s', id_usuario)
            raise Exception('No se pudo crear ventas_borrador')

        for item in carrito_sesion:
            id_prod = item.get('id')
            cant = int(item.get('cantidad', 1))
            if item.get('es_combo'):
                combo = Combo.query.get(int(id_prod))
                if not combo:
                    raise Exception(f'Combo no encontrado: {id_prod}')
                precio = float(combo.precio_venta)
                db.session.execute(
                    db.text("INSERT INTO detalle_ventas_borrador (id_venta_borrador, id_combo, cantidad, precio_unitario) VALUES (:vb, :id_combo, :cant, :precio)"),
                    {'vb': id_vb, 'id_combo': id_prod, 'cant': cant, 'precio': precio}
                )
            else:
                producto = Producto.query.get(int(id_prod))
                if not producto:
                    raise Exception(f'Producto no encontrado: {id_prod}')
                precio = float(producto.precio_venta)
                db.session.execute(
                    db.text("INSERT INTO detalle_ventas_borrador (id_venta_borrador, id_producto, cantidad, precio_unitario) VALUES (:vb, :id_prod, :cant, :precio)"),
                    {'vb': id_vb, 'id_prod': id_prod, 'cant': cant, 'precio': precio}
                )
        db.session.commit()
        current_app.logger.info('Item transferido a carrito BD: usuario=%s producto=%s cantidad=%s', id_usuario, id_prod, cant)

        # 3) Preparar datos adicionales necesarios por el SP
        # Obtener nombre del método para validar parámetros (tarjeta/efectivo)
        metodo_obj = None
        if id_metodo:
            metodo_obj = MetodoPago.query.get(id_metodo)
        metodo_nombre = metodo_obj.nombre.lower() if metodo_obj and metodo_obj.nombre else ''

        # Obtener total desde la vista de resumen para casos de efectivo
        resumen = None
        try:
            resumen = db.session.execute(db.text("SELECT total FROM vw_carrito_resumen WHERE id_usuario = :id_usuario LIMIT 1"), {'id_usuario': id_usuario}).mappings().first()
        except Exception:
            resumen = None

        total_carrito = resumen.get('total') if resumen and resumen.get('total') is not None else None

        # Si es efectivo y no enviaron monto, usar el total como monto recibido
        if metodo_nombre == 'efectivo' and (monto_recibido is None or float(monto_recibido) <= 0):
            if total_carrito is None:
                flash('No fue posible determinar el total del carrito para pago en efectivo.', 'error')
                return redirect(url_for('pagina.carrito_ver'))
            monto_recibido = float(total_carrito)

        # Si es tarjeta, validar que venga numero de cuenta
        if metodo_nombre == 'tarjeta' and (not num_cuenta or num_cuenta.strip() == ''):
            flash('Debes ingresar el número de la cuenta/tarjeta para procesar el pago con tarjeta.', 'error')
            return redirect(url_for('pagina.carrito_ver'))

        # 3) Llamada raw a la BD para ejecutar el SP de venta (manejo de resultsets similar a ventas)
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        try:
            current_app.logger.info('Llamando a sp_venta_completar usuario=%s metodo=%s total=%s', id_usuario, id_metodo, total_carrito)
            cursor.callproc('sp_venta_completar', (id_usuario, id_metodo, num_cuenta, monto_recibido))

            id_venta = None
            if hasattr(cursor, 'stored_results'):
                for rs in cursor.stored_results():
                    row = rs.fetchone()
                    if row is not None:
                        id_venta = row[0]
                        current_app.logger.info('sp_venta_completar devolvió id_venta=%s', id_venta)
            else:
                row = cursor.fetchone()
                if row is not None:
                    id_venta = row[0]
                while cursor.nextset():
                    row = cursor.fetchone()
                    if row is not None:
                        id_venta = row[0]

            connection.commit()
            current_app.logger.info('sp_venta_completar commit realizado, id_venta=%s', id_venta)

            # Asegurar ticket creado (pago_online flow)
            try:
                t = db.session.execute(db.text("SELECT id_ticket FROM tickets WHERE id_venta = :idv LIMIT 1"), {'idv': id_venta}).mappings().first()
                if not t:
                    total_row = db.session.execute(db.text("SELECT total FROM ventas WHERE id_venta = :idv LIMIT 1"), {'idv': id_venta}).mappings().first()
                    monto_pagado = float(total_row['total']) if total_row and total_row.get('total') is not None else 0.00
                    folio = db.session.execute(db.text("SELECT CONCAT('TKT-', LPAD(:idv, 8, '0')) AS folio"), {'idv': id_venta}).scalar()
                    db.session.execute(db.text("INSERT INTO tickets (id_venta, folio, monto_pagado) VALUES (:idv, :folio, :monto)"), {'idv': id_venta, 'folio': folio, 'monto': monto_pagado})
                    db.session.commit()
                    current_app.logger.info('Ticket creado manualmente (pago_online) id_venta=%s folio=%s monto=%s', id_venta, folio, monto_pagado)
            except Exception:
                db.session.rollback()
                current_app.logger.exception('Error asegurando ticket para venta %s (pago_online)', id_venta)

        except Exception as e:
            connection.rollback()
            current_app.logger.exception(e)
            raise
        finally:
            cursor.close()
            connection.close()

        # Guardar ticket para imprimir y limpiar carrito de sesión
        session['ticket_a_imprimir'] = id_venta
        _save_carrito([])
        flash('Pago procesado correctamente. Gracias por tu compra.', 'success')
        return redirect(url_for('pagina.carrito_ver'))

    except (OperationalError, DBAPIError, Exception) as e:
        db.session.rollback()
        current_app.logger.exception(e)
        mensaje_usuario = 'Ocurrió un error al procesar el pago.'
        try:
            if hasattr(e, 'orig') and getattr(e.orig, 'args', None):
                codigo_mysql = e.orig.args[0]
                mensaje_mysql = e.orig.args[1] if len(e.orig.args) > 1 else str(e.orig)
                if codigo_mysql == 1644:
                    mensaje_usuario = mensaje_mysql
                else:
                    mensaje_usuario = mensaje_mysql
            else:
                mensaje_usuario = str(e)
        except Exception:
            try:
                mensaje_usuario = str(e)
            except Exception:
                pass
        flash(mensaje_usuario, 'error')
        return redirect(url_for('pagina.carrito_ver'))
