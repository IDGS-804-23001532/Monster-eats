from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Producto, SolicitudProduccion
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
import random
from audit_logger import audit  # <--- IMPORTAMOS EL LOGGER DE MONGODB

solicitud_produccion = Blueprint('solicitud_produccion', __name__, url_prefix='/solicitud-produccion')

# ==============================================================================
# ZONA DE VENTAS / PEDIDOS (Exclusivo para Cliente, Cajero y Cocina)
# ==============================================================================

@solicitud_produccion.route('/')
@login_required
@roles_accepted('Cliente', 'cliente', 'Cajero', 'cajero', 'cocina', 'cliente')
def principal():
    productos = Producto.query.filter_by(activo=1).all()
    
    if 'carrito' not in session:
        session['carrito'] = {}
        
    total_carrito = sum(item['precio'] * item['cantidad'] for item in session['carrito'].values())
    ultimo_ticket = session.pop('ultimo_ticket', None)
    
    return render_template('solicitud_Produccion/principal.html', 
                           productos=productos, 
                           carrito=session['carrito'], 
                           total_carrito=total_carrito,
                           ultimo_ticket=ultimo_ticket)

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
    session.modified = True
    flash(f'¡{cantidad}x {producto.nombre} agregado a tu orden!', 'success')
        
    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/confirmar', methods=['POST'])
@login_required
@roles_accepted('Cliente', 'cliente', 'Cajero', 'cajero', 'Cocina', 'cocina', 'Gerente', 'gerente')
def confirmar_pedido():
    carrito = session.get('carrito', {})
    metodo_pago = request.form.get('metodo_pago', 'Efectivo')
    
    if not carrito:
        flash('Tu orden está vacía. Agrega productos primero.', 'error')
        return redirect(url_for('solicitud_produccion.principal'))
        
    try:
        total_pagar = 0
        productos_ticket = []
        
        for prod_id, item in carrito.items():
            # Generamos la solicitud que viajará a la ruta de Cocina
            nueva_solicitud = SolicitudProduccion(
                id_usuario_solicita=current_user.id_usuario,
                id_producto=int(prod_id),
                cantidad=item['cantidad'],
                estado='Pendiente'
            )
            db.session.add(nueva_solicitud)
            
            subtotal = item['precio'] * item['cantidad']
            total_pagar += subtotal
            productos_ticket.append({'nombre': item['nombre'], 'cantidad': item['cantidad']})
            
        db.session.commit()
        
        num_ticket = random.randint(100, 999)
        
        session['ultimo_ticket'] = {
            'num_orden': num_ticket,
            'cliente': current_user.email,
            'productos': productos_ticket,
            'total': total_pagar,
            'metodo': metodo_pago
        }
        
        # --- REGISTRO DE AUDITORÍA MONGODB: PEDIDO CREADO ---
        audit.log_action(
            module_name="logs_produccion",
            action="Nuevo Pedido Creado",
            details={
                "num_ticket": num_ticket,
                "total_pagado": total_pagar,
                "metodo_pago": metodo_pago,
                "articulos": productos_ticket
            },
            level="INFO"
        )
        
        session.pop('carrito', None)
        
    except Exception as e:
        db.session.rollback()
        print(f"Error procesando pedido web: {e}")
        flash('Hubo un problema procesando tu orden. Intenta de nuevo.', 'error')
        
    return redirect(url_for('solicitud_produccion.principal'))

@solicitud_produccion.route('/vaciar', methods=['POST'])
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
@roles_accepted('Cocina', 'cocina', 'Gerente', 'gerente')
def completar_solicitud(id_solicitud):
    try:
        db.session.execute(text("CALL sp_completar_solicitud(:id)"), {'id': id_solicitud})
        db.session.commit()
        
        # --- REGISTRO DE AUDITORÍA MONGODB: PLATILLO DESPACHADO ---
        audit.log_action(
            module_name="logs_produccion",
            action="Comanda Completada en Cocina",
            details={
                "id_solicitud_produccion": id_solicitud
            },
            level="INFO"
        )
        
        flash('¡Platillo marcado como LISTO! El Cajero ha sido notificado.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error completando solicitud: {e}")
        flash('Hubo un error al intentar despachar la orden.', 'error')
        
    return redirect(url_for('solicitud_produccion.tablero_cocina'))