from flask import render_template, request, abort
from Pagina import pagina_bp
from models import db, Producto, CategoriaProducto, Combo, Receta, Insumo, UnidadMedida

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
