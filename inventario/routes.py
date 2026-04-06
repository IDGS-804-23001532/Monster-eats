from flask import render_template, request, url_for, redirect, flash
from models import Insumo, LoteInsumo, UnidadMedida, db
from sqlalchemy import func as sql_func, text, case
from flask_security import current_user
from forms import MermaForm
from . import inventario
import datetime
from audit_logger import audit

@inventario.route('/inventario')
def index():
    hoy = datetime.date.today()
    
    #Busqueda de insumos
    search_query = request.args.get('search_query', '')
    
    # Subconsulta para obtener la última fecha de movimiento
    from models import MovimientoInventarioInsumo
    last_move_subq = db.session.query(
        MovimientoInventarioInsumo.id_insumo,
        sql_func.max(MovimientoInventarioInsumo.fecha_movimiento).label('ultima_mov')
    ).group_by(MovimientoInventarioInsumo.id_insumo).subquery()

    # Consulta principal refinada
    stock_query = db.session.query(
        Insumo.id_insumo,
        Insumo.nombre,
        Insumo.id_unidad_medida,
        Insumo.costo_unitario,
        Insumo.porcentaje_merma,
        Insumo.activo,
        sql_func.coalesce(sql_func.sum(
            case(
                (LoteInsumo.fecha_caducidad >= hoy, LoteInsumo.cantidad_disponible),
                else_=0
            )
        ), 0).label('stock_actual'),
        sql_func.count(LoteInsumo.id_lote).label('num_lotes'),
        sql_func.min(LoteInsumo.fecha_caducidad).label('prox_caducidad'),
        last_move_subq.c.ultima_mov.label('ultima_act')
    ).outerjoin(LoteInsumo, (Insumo.id_insumo == LoteInsumo.id_insumo) & (LoteInsumo.cantidad_disponible > 0)
    ).outerjoin(last_move_subq, Insumo.id_insumo == last_move_subq.c.id_insumo
    ).group_by(
        Insumo.id_insumo, Insumo.nombre, Insumo.id_unidad_medida, 
        Insumo.costo_unitario, Insumo.porcentaje_merma, Insumo.activo,
        last_move_subq.c.ultima_mov
    )
    
    if search_query:
        stock_query = stock_query.filter(Insumo.nombre.ilike(f'%{search_query}%'))
    
    stock_query = stock_query.order_by(Insumo.nombre).all()
    
    # Mapeo de unidades para búsqueda rápida
    from models import UnidadMedida
    unidades = {u.id_unidad_medida: u for u in UnidadMedida.query.all()}
    
    # Construimos la lista para el template
    inventario_list = []
    for row in stock_query:
        um = unidades.get(row.id_unidad_medida)
        
        # Buscamos el ID del lote que está por caducar (el que tiene la fecha mínima)
        prox_lote = db.session.query(LoteInsumo.id_lote).filter(
            LoteInsumo.id_insumo == row.id_insumo,
            LoteInsumo.cantidad_disponible > 0,
            LoteInsumo.fecha_caducidad >= hoy
        ).order_by(LoteInsumo.fecha_caducidad.asc()).first()

        inventario_list.append({
            'id_insumo': row.id_insumo,
            'nombre': row.nombre,
            'unidad': um.nombre if um else 'S/N',
            'abreviatura': um.abreviatura if um else '',
            'costo_unitario': row.costo_unitario,
            'porcentaje_merma': row.porcentaje_merma,
            'activo': row.activo,
            'stock_actual': float(row.stock_actual or 0),
            'num_lotes': row.num_lotes,
            'prox_caducidad': row.prox_caducidad,
            'prox_lote_id': prox_lote.id_lote if prox_lote else None,
            'ultima_act': row.ultima_act
        })
    
    # Detalle de un insumo específico (ver lotes)
    detalle_insumo = None
    lotes_all = []
    show_modal = None
    caducidad_proxima = hoy + datetime.timedelta(days=30)
    
    ver_id = request.args.get('ver')
    if ver_id:
        detalle_insumo = Insumo.query.get(ver_id)
        if detalle_insumo:
            # Traemos solo los lotes con stock disponible
            lotes_all = LoteInsumo.query.filter(
                LoteInsumo.id_insumo == ver_id,
                LoteInsumo.cantidad_disponible > 0
            ).order_by(LoteInsumo.fecha_caducidad.asc()).all()
            show_modal = 'detalleInsumoModal'
    
    # Instanciamos el formulario de merma para el modal de registro
    merma_form = MermaForm()

    # Consultamos el historial de mermas usando tu vista
    mermas_historial = []
    try:
        from sqlalchemy import text
        query_h = text("SELECT * FROM v_mermas_detallado ORDER BY fecha DESC, hora DESC LIMIT 50")
        mermas_historial = db.session.execute(query_h).fetchall()
    except Exception as e:
        print(f"Error al cargar historial: {e}")

    return render_template('inventario/index.html', 
                          inventario=inventario_list, 
                          search_query=search_query, 
                          detalle_insumo=detalle_insumo,
                          lotes_all=lotes_all,
                          show_modal=show_modal,
                          hoy=hoy,
                          caducidad_proxima=caducidad_proxima,
                          merma_form=merma_form,
                          mermas_historial=mermas_historial)

@inventario.route('/registrar_merma', methods=['POST'])
def registrar_merma():
    form = MermaForm(request.form)
    id_insumo = form.id_insumo.data
    
    if form.validate():
        id_lote = form.id_lote.data
        cantidad = form.cantidad.data
        motivo = form.motivo.data
        id_usuario = current_user.id_usuario

        try:
            # 1. Llamar al procedimiento 
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

            # 2. Descontar stock manualmente del lote (Aseguramos que baje el inventario)
            lote = LoteInsumo.query.get(id_lote)
            if lote:
                # Regresamos a > para permitir retirar el TOTAL del lote si es necesario (ej. si tengo 10, puedo retirar 10)
                if float(cantidad) > float(lote.cantidad_disponible):
                    flash(f"Error: La cantidad a retirar ({cantidad}) es mayor al stock disponible ({lote.cantidad_disponible})", "danger")
                    return redirect(url_for('inventario.index', ver=id_insumo))

                stock_anterior = float(lote.cantidad_disponible)
                lote.cantidad_disponible = float(lote.cantidad_disponible) - float(cantidad)
                
                # 3. Registrar el movimiento en el historial global
                from models import MovimientoInventarioInsumo
                nuevo_mov = MovimientoInventarioInsumo(
                    id_insumo=id_insumo,
                    id_lote=id_lote,
                    tipo_movimiento='SALIDA_MERMA',
                    cantidad=float(cantidad),
                    stock_anterior=stock_anterior,
                    stock_nuevo=float(lote.cantidad_disponible),
                    motivo=f"MERMA: {motivo}",
                    id_usuario=id_usuario,
                    referencia_tabla='mermas_log'
                )
                db.session.add(nuevo_mov)

            db.session.commit()
            
            # --- REGISTRO DE AUDITORÍA MONGO ---
            audit.log_action("Inventario", "MERMA", details={
                "id_insumo": id_insumo,
                "id_lote": id_lote,
                "cantidad": float(cantidad),
                "motivo": motivo
            })
            
            flash('Merma registrada y stock actualizado correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            if "No hay suficiente stock" in error_msg:
                flash('Error: No hay suficiente stock en el lote', 'danger')
            elif "El lote no existe" in error_msg:
                flash('Error: El lote seleccionado no existe', 'danger')
            else:
                flash(f'Error al registrar merma: {error_msg}', 'danger')
    else:
        # Si la validación de WTForms falla, mostramos los errores
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en {getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('inventario.index', ver=id_insumo))

@inventario.route('/limpiar_busqueda_inventario')
def limpiar_busqueda():
    return redirect(url_for('inventario.index'))
