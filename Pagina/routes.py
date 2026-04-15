from flask import render_template, request, abort, session, redirect, url_for, flash
from sqlalchemy.exc import OperationalError, DBAPIError
from Pagina import pagina_bp
from models import db, Producto, CategoriaProducto, Combo, Receta, Insumo, UnidadMedida, MetodoPago
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
            productos.append({
                'nombre':       c.nombre,
                'precio_venta': c.precio_venta,
                'imagen':       c.imagen or 'default_combo.png',
                'es_combo':     True,
                'id_combo':     c.id_combo,
                'id_producto':  None,
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
        if q:
            productos = Producto.query.filter(
                Producto.id_categoria == cat.id_categoria,
                Producto.activo == True,
                Producto.nombre.ilike(f"%{q}%")
            ).all()
        else:
            productos = Producto.query.filter_by(id_categoria=cat.id_categoria, activo=True).all()

    return render_template(
        'Pagina/Productos.html',
        productos=productos,
        categoria_nombre=nombre_cat,
        categoria_param=categoria,
        q=q
    )


# ── Detalle de Producto ──────────────────────────────────────────────────────

@pagina_bp.route('/producto/<int:id_producto>', methods=['GET'])
def producto_detalle(id_producto):
    producto = Producto.query.filter_by(id_producto=id_producto, activo=True).first_or_404()
    categoria = CategoriaProducto.query.get(producto.id_categoria)
    ingredientes = _get_ingredientes(id_producto)
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
    )


# ── Carrito (sesión) ─────────────────────────────────────────────────────────

def _get_carrito():
    """Obtiene la lista de items del carrito desde la sesión."""
    return session.get('carrito', [])

def _save_carrito(carrito):
    """Guarda la lista de items del carrito en la sesión."""
    session['carrito'] = carrito


@pagina_bp.route('/carrito/agregar', methods=['POST'])
@login_required
def carrito_agregar():
    """Agrega un producto o combo al carrito desde la página de descripción."""
    id_producto = request.form.get('id_producto', type=int)
    id_combo    = request.form.get('id_combo', type=int)
    cantidad    = request.form.get('cantidad', 1, type=int)

    carrito = _get_carrito()

    if id_combo:
        combo = Combo.query.get_or_404(id_combo)
        key = f'combo_{id_combo}'
        # Buscar si ya existe en el carrito
        for item in carrito:
            if item['key'] == key:
                item['cantidad'] += cantidad
                _save_carrito(carrito)
                flash(f'{combo.nombre} actualizado en tu pedido.', 'success')
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
                flash(f'{producto.nombre} actualizado en tu pedido.', 'success')
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
        flash('Producto no encontrado.', 'error')
        return redirect(request.referrer or '/')

    _save_carrito(carrito)
    flash('Producto añadido a tu pedido.', 'success')
    return redirect(request.referrer or '/')


@pagina_bp.route('/carrito/action', methods=['POST'])
@login_required
def carrito_action():
    """Maneja las acciones del carrito: +1, -1, eliminar, vaciar, confirmar."""
    accion   = request.form.get('accion')
    item_key = request.form.get('item_key')
    carrito  = _get_carrito()

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

    elif accion == 'confirmar':
        numero_cuenta = request.form.get('numero_cuenta', '').strip()
        if not carrito:
            flash('Tu carrito está vacío.', 'error')
        elif not numero_cuenta or len(numero_cuenta) < 16 or not numero_cuenta.isdigit():
            flash('Ingresa un número de tarjeta válido (16-20 dígitos).', 'error')
        else:
            try:
                # Obtener id del método de pago "Tarjeta"
                metodo_tarjeta = MetodoPago.query.filter(
                    MetodoPago.nombre.ilike('tarjeta')
                ).first()
                if not metodo_tarjeta:
                    flash('Método de pago no disponible.', 'error')
                    return redirect(url_for('pagina.carrito_ver'))

                # Usar un usuario genérico para pedidos web (id_usuario = 1 u otro)
                id_usuario_web = 1

                # 1) Limpiar carrito del usuario en BD (por si quedó algo)
                db.session.execute(
                    db.text("DELETE FROM carrito WHERE id_usuario = :uid"),
                    {'uid': id_usuario_web}
                )
                db.session.commit()

                # 2) Transferir items de la sesión al carrito de BD
                for item in carrito:
                    id_prod = item['id']
                    cant = item['cantidad']
                    db.session.execute(
                        db.text("CALL sp_carrito_agregar(:id_usuario, :id_producto, :cantidad)"),
                        {'id_usuario': id_usuario_web, 'id_producto': id_prod, 'cantidad': cant}
                    )
                    db.session.commit()

                # 3) Completar la venta con tarjeta
                result = db.session.execute(
                    db.text("CALL sp_venta_completar(:id_usuario, :id_metodo_pago, :num_cuenta, :monto_recibido)"),
                    {
                        'id_usuario': id_usuario_web,
                        'id_metodo_pago': metodo_tarjeta.id_metodo_pago,
                        'num_cuenta': numero_cuenta,
                        'monto_recibido': 0
                    }
                )
                db.session.commit()

                _save_carrito([])
                flash('¡Pago procesado! Tu pedido está siendo preparado. Pasa por tu pedido al mostrador.', 'success')

            except (OperationalError, DBAPIError) as e:
                db.session.rollback()
                mensaje = 'Error al procesar el pago.'
                try:
                    if e.orig.args[0] == 1644:
                        mensaje = e.orig.args[1]
                except Exception:
                    pass
                flash(mensaje, 'error')

    return redirect(url_for('pagina.carrito_ver'))


@pagina_bp.route('/carrito', methods=['GET'])
@login_required
def carrito_ver():
    """Muestra la página del carrito."""
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
    )
