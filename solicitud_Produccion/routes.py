from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Producto, SolicitudProduccion, OrdenProduccion
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
import random
from audit_logger import audit  # <--- IMPORTAMOS EL LOGGER DE MONGODB

solicitud_produccion = Blueprint('solicitud_produccion', __name__, url_prefix='/solicitud-produccion')

@solicitud_produccion.route('/')
@login_required
@roles_accepted('Cliente', 'cliente', 'Cajero', 'cajero', 'Cocina', 'cocina', 'Gerente', 'gerente', 'cocinero')
def principal():
    # Obtenemos productos activos para el formulario de petición
    productos = Producto.query.filter_by(activo=1).all()
    
    # --- LOGICA DEL CARRITO (HEAD) ---
    if 'carrito' not in session:
        session['carrito'] = {}
        
    total_carrito = sum(item['precio'] * item['cantidad'] for item in session['carrito'].values())
    ultimo_ticket = session.pop('ultimo_ticket', None)
    
    # --- LÓGICA DE VISTAS POR ROL (AXEL / REMOTE) ---
    if current_user.has_role('Cocina') or current_user.has_role('cocina') or current_user.has_role('cocinero'):
        # La cocina ve todas las peticiones pendientes para aprobarlas
        solicitudes = SolicitudProduccion.query.filter(
            SolicitudProduccion.estado.in_(['Pendiente', 'En Proceso'])
        ).order_by(SolicitudProduccion.fecha_solicitud.desc()).all()
    else:
        # El Cajero o el Cliente ven solo las peticiones que ellos han hecho
        solicitudes = SolicitudProduccion.query.filter_by(
            id_usuario_solicita=current_user.id_usuario
        ).order_by(SolicitudProduccion.fecha_solicitud.desc()).limit(20).all()

    return render_template('solicitud_Produccion/principal.html', 
                           productos=productos, 
                           carrito=session['carrito'], 
                           total_carrito=total_carrito,
                           ultimo_ticket=ultimo_ticket,
                           solicitudes=solicitudes)

@solicitud_produccion.route('/agregar/<int:id_producto>', methods=['POST'])
@login_required
@roles_accepted('Cliente', 'cliente', 'Cajero', 'cajero', 'Cocina', 'cocina', 'Gerente', 'gerente')
def agregar_carrito(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    cantidad = int(request.form.get('cantidad', 1))
    
    carrito = session.get('carrito', {})
    prod_id_str = str(id_producto)
    
    if prod_id_str in carrito:
        carrito[prod_id_str]['cantidad'] += cantidad
    else:
        carrito[prod_id_str] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio_venta),
            'cantidad': cantidad
        }
    
    session['carrito'] = carrito
    flash(f'{producto.nombre} agregado al carrito.', 'success')
    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/crear', methods=['POST'])
@login_required
@roles_accepted('Gerente', 'gerente', 'Cajero', 'cajero')
def crear_solicitud():
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad')

    try:
        # CREACIÓN DE LA PETICIÓN (No descuenta inventario, solo avisa)
        nueva_solicitud = SolicitudProduccion(
            id_usuario_solicita=current_user.id_usuario,
            id_producto=id_producto,
            cantidad=cantidad,
            estado='Pendiente'
        )
        db.session.add(nueva_solicitud)
        db.session.commit()

        audit.log_action(module_name="logs_solicitud_produccion", action="Crear Petición Reabastecimiento", details={"id_producto": id_producto, "cantidad": cantidad})
        flash('Petición de reabastecimiento enviada a cocina.', 'success')
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Error al crear la petición.', 'error')

    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/aprobar/<int:id_solicitud>', methods=['POST'])
@login_required
@roles_accepted('Gerente', 'gerente', 'Cocina', 'cocina', 'cocinero')
def aprobar_solicitud(id_solicitud):
    solicitud = SolicitudProduccion.query.get_or_404(id_solicitud)
    
    try:
        # 1. El chef aprueba la solicitud y el sistema crea la Orden de Producción Real
        nueva_orden = OrdenProduccion(
            id_producto=solicitud.id_producto,
            id_usuario_crea=current_user.id_usuario,
            cantidad_programada=solicitud.cantidad,
            estado='Pendiente'
        )
        db.session.add(nueva_orden)
        db.session.flush() # Flush nos permite obtener el ID generado sin hacer commit final aún

        # 2. Vinculamos el aviso (solicitud) con la orden de fábrica (orden_produccion)
        solicitud.id_orden_produccion = nueva_orden.id_orden_produccion
        solicitud.estado = 'En Proceso' # Avisamos al cajero que ya lo están haciendo
        
        db.session.commit()

        audit.log_action(module_name="logs_solicitud_produccion", action="Aprobar Petición y Crear Orden", details={"id_solicitud": id_solicitud, "id_orden": nueva_orden.id_orden_produccion})
        flash('Petición aprobada. Se ha generado la Orden de Producción formal.', 'success')
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Error al aprobar la petición.', 'error')

    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/rechazar/<int:id_solicitud>', methods=['POST'])
@login_required
@roles_accepted('Gerente', 'gerente', 'Cocina', 'cocina', 'cocinero')
def rechazar_solicitud(id_solicitud):
    solicitud = SolicitudProduccion.query.get_or_404(id_solicitud)
    try:
        solicitud.estado = 'Cancelada'
        db.session.commit()
        audit.log_action(module_name="logs_solicitud_produccion", action="Rechazar Petición", details={"id_solicitud": id_solicitud})
        flash('Petición de reabastecimiento rechazada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al rechazar la petición.', 'error')

    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/confirmar_pedido', methods=['POST'])
@login_required
@roles_accepted('Cliente', 'cliente', 'Cajero', 'cajero', 'Cocina', 'cocina', 'Gerente', 'gerente')
def confirmar_pedido():
    carrito = session.get('carrito', {})
    if not carrito:
        flash('No tienes productos en el carrito.', 'error')
        return redirect(url_for('solicitud_produccion.principal'))
    
    metodo_pago = request.form.get('metodo_pago', 'Efectivo')
    
    # Simulación de pago y envío de pedido
    session.pop('carrito', None)
    ticket_id = f"TICK-{random.randint(1000, 9999)}"
    session['ultimo_ticket'] = ticket_id
    
    flash(f'¡Pedido confirmado con éxito! Ticket: {ticket_id}', 'success')
    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/vaciar_carrito', methods=['POST'])
@login_required
@roles_accepted('Cliente', 'cliente', 'Cajero', 'cajero', 'Cocina', 'cocina', 'Gerente', 'gerente')
def vaciar_carrito():
    session.pop('carrito', None)
    flash('Carrito vaciado correctamente.', 'success')
    return redirect(url_for('solicitud_produccion.principal'))


# ==============================================================================
# ZONA DE COCINA / KDS (Exclusivo para el Cocinero)
# ==============================================================================

@solicitud_produccion.route('/tablero')
@login_required
@roles_accepted('Cocina', 'cocina', 'Gerente', 'gerente', 'cocinero') 
def tablero_cocina():
    try:
        query = text("SELECT * FROM vw_tablero_cocina")
        solicitudes = db.session.execute(query).mappings().fetchall()
        
        # Renderiza la vista de las comandas
        return render_template('solicitud_Produccion/tablero.html', solicitudes=solicitudes)
    except Exception as e:
        print(f"Error cargando Tablero KDS: {e}")
        flash('Error de conexión con la base de datos de comandas.', 'error')
        return redirect(url_for('dashboard.index'))

@solicitud_produccion.route('/completar/<int:id_solicitud>', methods=['POST'])
@login_required
@roles_accepted('Cocina', 'cocina', 'Gerente', 'gerente', 'cocinero')
def completar_solicitud(id_solicitud):
    try:
        db.session.execute(text("CALL sp_completar_solicitud(:id)"), {'id': id_solicitud})
        db.session.commit()
        flash('Comanda completada con éxito.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error completando comanda: {e}")
        flash('Error al completar la comanda.', 'error')
    
    return redirect(url_for('solicitud_produccion.tablero_cocina'))