from flask import render_template, request, redirect, url_for, flash
from models import db
from sqlalchemy import text
import logging
from . import produccion_bp
import forms

logger = logging.getLogger(__name__)

# ==========================================================================
# LISTADO DE ÓRDENES DE PRODUCCIÓN
# ==========================================================================

@produccion_bp.route('/')
def index():
    search = request.args.get('search', '')
    estado = request.args.get('estado', '')
    
    try:
        # Construir consulta base
        query_sql = """
            SELECT * FROM V_OrdenesProduccion
            WHERE 1=1
        """
        params = {}
        
        if search:
            query_sql += " AND producto LIKE :search"
            params['search'] = f'%{search}%'
        
        if estado and estado != 'todos':
            query_sql += " AND estado = :estado"
            params['estado'] = estado
        
        query_sql += " ORDER BY fecha_creacion DESC"
        
        ordenes = db.session.execute(text(query_sql), params).fetchall()
        db.session.commit()
        
        return render_template('produccion/index.html', 
                             ordenes=ordenes, 
                             search=search, 
                             estado=estado)
    
    except Exception as e:
        logger.error(f"Error en index de producción: {str(e)}")
        flash('Error al cargar las órdenes de producción', 'danger')
        return render_template('produccion/index.html', ordenes=[])

# ==========================================================================
# CREAR NUEVA ORDEN DE PRODUCCIÓN
# ==========================================================================

@produccion_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    # Obtener productos para el select
    productos = db.session.execute(text("""
        SELECT id_producto, nombre, precio_venta 
        FROM productos 
        WHERE activo = 1 
        ORDER BY nombre
    """)).fetchall()
    db.session.commit()
    
    form = forms.ProduccionOrdenForm()
    form.id_producto.choices = [(p[0], f"{p[1]} - ${float(p[2]):.2f}") for p in productos]
    
    if form.validate_on_submit():
        try:
            # Ejecutar SP para crear orden
            result = db.session.execute(
                text("CALL SP_Produccion_CrearOrden(:id_producto, :id_usuario, :cantidad, :observaciones)"),
                {
                    'id_producto': form.id_producto.data,
                    'id_usuario': 2,  # TODO: Obtener del usuario logueado
                    'cantidad': form.cantidad_programada.data,
                    'observaciones': form.observaciones.data or ''
                }
            )
            db.session.commit()
            
            # Obtener el ID de la orden creada
            orden_id = result.fetchone()[0] if result else None
            db.session.commit()
            
            flash('Orden de producción creada exitosamente', 'success')
            return redirect(url_for('produccion.detalle', id=orden_id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear orden: {str(e)}")
            flash(f'Error al crear la orden: {str(e)}', 'danger')
    
    return render_template('produccion/crear.html', form=form)

# ==========================================================================
# DETALLE DE ORDEN DE PRODUCCIÓN
# ==========================================================================

@produccion_bp.route('/detalle/<int:id>')
def detalle(id):
    try:
        # 1. Obtener información de la orden usando SQL directo
        orden = db.session.execute(
            text("""
                SELECT 
                    op.id_orden_produccion,
                    op.id_producto,
                    p.nombre AS producto,
                    p.precio_venta,
                    op.cantidad_programada,
                    op.cantidad_producida,
                    op.estado,
                    op.fecha_creacion,
                    op.fecha_inicio,
                    op.fecha_finalizacion,
                    op.observaciones,
                    u1.email AS creado_por,
                    u2.email AS responsable
                FROM ordenes_produccion op
                JOIN productos p ON op.id_producto = p.id_producto
                LEFT JOIN usuarios u1 ON op.id_usuario_crea = u1.id_usuario
                LEFT JOIN usuarios u2 ON op.id_usuario_responsable = u2.id_usuario
                WHERE op.id_orden_produccion = :id
            """),
            {'id': id}
        ).fetchone()
        
        if not orden:
            flash('Orden no encontrada', 'danger')
            return redirect(url_for('produccion.index'))
        
        # 2. Obtener insumos necesarios para esta producción
        insumos = db.session.execute(
            text("""
                SELECT 
                    i.nombre AS insumo,
                    um.abreviatura,
                    r.cantidad_requerida,
                    (r.cantidad_requerida * :cantidad) AS cantidad_total,
                    i.costo_unitario,
                    (r.cantidad_requerida * :cantidad) * i.costo_unitario AS costo_total
                FROM recetas r
                JOIN insumos i ON r.id_insumo = i.id_insumo
                JOIN unidades_medida um ON i.id_unidad_medida = um.id_unidad_medida
                WHERE r.id_producto = :id_producto
                ORDER BY i.nombre
            """),
            {
                'id_producto': orden.id_producto,
                'cantidad': orden.cantidad_programada
            }
        ).fetchall()
        
        # 3. Validar stock (usando SQL directo)
        stock_result = db.session.execute(
            text("""
                SELECT 
                    CASE 
                        WHEN EXISTS (
                            SELECT 1 
                            FROM recetas r
                            WHERE r.id_producto = :id_producto
                            AND (
                                SELECT COALESCE(SUM(li.cantidad_disponible), 0)
                                FROM lotes_insumo li
                                WHERE li.id_insumo = r.id_insumo
                            ) < (r.cantidad_requerida * :cantidad)
                        ) THEN 0
                        ELSE 1
                    END AS stock_suficiente
            """),
            {
                'id_producto': orden.id_producto,
                'cantidad': orden.cantidad_programada
            }
        ).fetchone()
        
        stock_suficiente = stock_result.stock_suficiente if stock_result else False
        
        # Agregar mensaje descriptivo según el estado del stock
        if stock_suficiente:
            mensaje_stock = "Stock suficiente para iniciar producción"
        else:
            # Obtener detalles de qué insumos faltan
            insumos_faltantes = db.session.execute(
                text("""
                    SELECT 
                        i.nombre AS insumo,
                        um.abreviatura,
                        r.cantidad_requerida * :cantidad AS cantidad_necesaria,
                        COALESCE(SUM(li.cantidad_disponible), 0) AS stock_actual
                    FROM recetas r
                    JOIN insumos i ON r.id_insumo = i.id_insumo
                    JOIN unidades_medida um ON i.id_unidad_medida = um.id_unidad_medida
                    LEFT JOIN lotes_insumo li ON i.id_insumo = li.id_insumo
                    WHERE r.id_producto = :id_producto
                    GROUP BY i.id_insumo, i.nombre, um.abreviatura, r.cantidad_requerida
                    HAVING stock_actual < (r.cantidad_requerida * :cantidad)
                """),
                {
                    'id_producto': orden.id_producto,
                    'cantidad': orden.cantidad_programada
                }
            ).fetchall()
            
            if insumos_faltantes:
                faltantes_texto = ", ".join([f"{f.insumo} (falta {float(f.cantidad_necesaria - f.stock_actual):.4f} {f.abreviatura})" for f in insumos_faltantes])
                mensaje_stock = f"Stock insuficiente. Faltan: {faltantes_texto}"
            else:
                mensaje_stock = "No hay suficiente stock de materia prima para esta producción"
        
        db.session.commit()
        
        return render_template('produccion/detalle.html', 
                             orden=orden, 
                             insumos=insumos,
                             stock_suficiente=stock_suficiente,
                             mensaje_stock=mensaje_stock)  # ← Agregada la variable
    
    except Exception as e:
        db.session.rollback()
        print(f"Error en detalle: {str(e)}")
        flash('Error al cargar el detalle de la orden', 'danger')
        return redirect(url_for('produccion.index'))    
# ==========================================================================
# INICIAR PRODUCCIÓN
# ==========================================================================

@produccion_bp.route('/iniciar/<int:id>', methods=['POST'])
def iniciar(id):
    try:
        # TODO: Obtener ID del usuario logueado
        id_usuario = 2  # Temporal, usar el del session
        
        db.session.execute(
            text("CALL SP_Produccion_Iniciar(:id_orden, :id_usuario)"),
            {'id_orden': id, 'id_usuario': id_usuario}
        )
        db.session.commit()
        
        flash('Producción iniciada. Los insumos han sido descontados del inventario.', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al iniciar producción {id}: {str(e)}")
        flash(f'Error al iniciar producción: {str(e)}', 'danger')
    
    return redirect(url_for('produccion.detalle', id=id))

# ==========================================================================
# FINALIZAR PRODUCCIÓN
# ==========================================================================

@produccion_bp.route('/finalizar/<int:id>', methods=['POST'])
def finalizar(id):
    cantidad_producida = request.form.get('cantidad_producida', type=int)
    
    if not cantidad_producida or cantidad_producida <= 0:
        flash('La cantidad producida debe ser mayor a 0', 'danger')
        return redirect(url_for('produccion.detalle', id=id))
    
    try:
        # TODO: Obtener ID del usuario logueado
        id_usuario = 2  # Temporal, usar el del session
        
        db.session.execute(
            text("CALL SP_Produccion_Finalizar(:id_orden, :cantidad, :id_usuario)"),
            {'id_orden': id, 'cantidad': cantidad_producida, 'id_usuario': id_usuario}
        )
        db.session.commit()
        
        flash(f'Producción finalizada. {cantidad_producida} unidades agregadas al inventario.', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al finalizar producción {id}: {str(e)}")
        flash(f'Error al finalizar producción: {str(e)}', 'danger')
    
    return redirect(url_for('produccion.detalle', id=id))

# ==========================================================================
# CANCELAR ORDEN
# ==========================================================================

@produccion_bp.route('/cancelar/<int:id>', methods=['POST'])
def cancelar(id):
    motivo = request.form.get('motivo', 'Cancelado por usuario')
    
    try:
        db.session.execute(
            text("CALL SP_Produccion_Cancelar(:id_orden, :motivo)"),
            {'id_orden': id, 'motivo': motivo}
        )
        db.session.commit()
        
        flash('Orden de producción cancelada', 'warning')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al cancelar orden {id}: {str(e)}")
        flash(f'Error al cancelar: {str(e)}', 'danger')
    
    return redirect(url_for('produccion.index'))