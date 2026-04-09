from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Producto, SolicitudProduccion, OrdenProduccion
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
import random
from audit_logger import audit  # <--- IMPORTAMOS EL LOGGER DE MONGODB

solicitud_produccion = Blueprint('solicitud_produccion', __name__, url_prefix='/solicitud-produccion')

@solicitud_produccion.route('/')
@login_required
@roles_accepted('Gerente', 'Cajero', 'Cocina')
def principal():
    # Obtenemos productos activos para el formulario de petición
    productos = Producto.query.filter_by(activo=1).all()
    
    # LÓGICA DE VISTAS POR ROL
    if current_user.has_role('Cocina'):
        # La cocina ve todas las peticiones pendientes para aprobarlas
        solicitudes = SolicitudProduccion.query.filter(
            SolicitudProduccion.estado.in_(['Pendiente', 'En Proceso'])
        ).order_by(SolicitudProduccion.fecha_solicitud.desc()).all()
    else:
        # El Cajero ve solo las peticiones que él ha hecho para saber si ya le hicieron caso
        solicitudes = SolicitudProduccion.query.filter_by(
            id_usuario_solicita=current_user.id_usuario
        ).order_by(SolicitudProduccion.fecha_solicitud.desc()).limit(20).all()

    return render_template('solicitud_Produccion/principal.html', productos=productos, solicitudes=solicitudes)

@solicitud_produccion.route('/crear', methods=['POST'])
@login_required
@roles_accepted('Gerente', 'Cajero')
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
@roles_accepted('Gerente', 'Cocina')
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
@roles_accepted('Gerente', 'Cocina')
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