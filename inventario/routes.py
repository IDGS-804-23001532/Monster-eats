from flask import render_template, request, url_for, redirect, flash
from models import Insumo, LoteInsumo, UnidadMedida, db
from sqlalchemy import func as sql_func, text
from flask_security import current_user
from . import inventario


@inventario.route('/inventario')
def index():
    search_query = request.args.get('search_query', '')
    
    # Consulta: stock por insumo (suma de cantidad_disponible de todos los lotes)
    stock_query = db.session.query(
        Insumo.id_insumo,
        Insumo.nombre,
        Insumo.costo_unitario,
        Insumo.porcentaje_merma,
        Insumo.activo,
        Insumo.id_unidad_medida,
        sql_func.coalesce(sql_func.sum(LoteInsumo.cantidad_disponible), 0).label('stock_actual'),
        sql_func.count(LoteInsumo.id_lote).label('num_lotes'),
        sql_func.min(LoteInsumo.fecha_caducidad).label('prox_caducidad')
    ).outerjoin(LoteInsumo, Insumo.id_insumo == LoteInsumo.id_insumo
    ).group_by(Insumo.id_insumo)
    
    if search_query:
        stock_query = stock_query.filter(Insumo.nombre.ilike(f'%{search_query}%'))
    
    stock_query = stock_query.order_by(Insumo.nombre).all()
    
    # Traemos las unidades para mostrar abreviatura
    unidades = {um.id_unidad_medida: um for um in UnidadMedida.query.all()}
    
    # Construimos la lista para el template
    inventario_list = []
    for row in stock_query:
        um = unidades.get(row.id_unidad_medida)
        inventario_list.append({
            'id_insumo': row.id_insumo,
            'nombre': row.nombre,
            'unidad': um.nombre if um else '',
            'abreviatura': um.abreviatura if um else '',
            'costo_unitario': row.costo_unitario,
            'porcentaje_merma': row.porcentaje_merma,
            'activo': row.activo,
            'stock_actual': float(row.stock_actual),
            'num_lotes': row.num_lotes,
            'prox_caducidad': row.prox_caducidad
        })
    
    # Detalle de un insumo específico (ver lotes)
    detalle_insumo = None
    lotes_all = []
    show_modal = None
    import datetime
    hoy = datetime.date.today()
    caducidad_proxima = hoy + datetime.timedelta(days=30)
    
    ver_id = request.args.get('ver')
    if ver_id:
        detalle_insumo = Insumo.query.get(ver_id)
        if detalle_insumo:
            lotes_all = LoteInsumo.query.filter_by(id_insumo=ver_id).order_by(LoteInsumo.fecha_caducidad.asc()).all()
            show_modal = 'detalleInsumoModal'

    return render_template('inventario/index.html',
                         inventario=inventario_list,
                         search_query=search_query,
                         detalle_insumo=detalle_insumo,
                         lotes_all=lotes_all,
                         hoy=hoy,
                         caducidad_proxima=caducidad_proxima,
                         show_modal=show_modal)

@inventario.route('/registrar_merma', methods=['POST'])
def registrar_merma():
    id_insumo = request.form.get('id_insumo')
    id_lote = request.form.get('id_lote')
    cantidad = request.form.get('cantidad')
    motivo = request.form.get('motivo')
    id_usuario = current_user.id_usuario

    try:
        # Ejecutamos el procedimiento almacenado
        db.session.execute(
            text("CALL sp_registrar_merma(:id_insumo, :id_lote, :cantidad, :motivo, :id_usuario)"),
            {
                'id_insumo': id_insumo,
                'id_lote': id_lote,
                'cantidad': cantidad,
                'motivo': motivo,
                'id_usuario': id_usuario
            }
        )
        db.session.commit()
        flash('Merma registrada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        # Intentamos obtener un mensaje más amable si viene del SIGNAL de SQL
        error_msg = str(e)
        if "No hay suficiente stock" in error_msg:
            flash('Error: No hay suficiente stock en el lote', 'danger')
        elif "El lote no existe" in error_msg:
            flash('Error: El lote seleccionado no existe', 'danger')
        else:
            flash(f'Error al registrar merma: {error_msg}', 'danger')

    return redirect(url_for('inventario.index', ver=id_insumo))

@inventario.route('/limpiar_busqueda_inventario')
def limpiar_busqueda():
    return redirect(url_for('inventario.index'))