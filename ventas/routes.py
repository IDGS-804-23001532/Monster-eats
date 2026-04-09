from flask import render_template, request, url_for, flash, redirect, session
from . import venta
from sqlalchemy.exc import OperationalError, DBAPIError
from models import db
from models import Venta, DetalleVenta, MetodoPago
from extensions import limiter
import forms
import pymysql
from datetime import datetime
from sanitizador import Sanitizador
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from audit_logger import audit

@venta.route('/ventas', methods=['GET', 'POST'])
@login_required
@roles_accepted('Cajero', 'Gerente', 'gerente')
@limiter.limit('20 per minute') # 8 request por minuto
def ventas():
    create_form = forms.VentasForm(request.form)

    lista_metodos = MetodoPago.query.all()
    create_form.metodo_pago.choices = [
        (str(mp.id_metodo_pago), mp.nombre) for mp in lista_metodos
    ]

    metodo_tarjeta = next(
        (mp for mp in lista_metodos if mp.nombre.lower() == 'tarjeta'),
        None
    )
    id_tarjeta = str(metodo_tarjeta.id_metodo_pago) if metodo_tarjeta else ''

    metodo_efectivo = next(
        (mp for mp in lista_metodos if mp.nombre.lower() == 'efectivo'),
        None
    )
    id_efectivo = str(metodo_efectivo.id_metodo_pago) if metodo_efectivo else ''

    id_usuario = current_user.id_usuario
    email_usuario = current_user.email # Extraemos el email para auditoría

    if request.method == 'POST':
        accion = request.form.get('accion')
        id_producto = request.form.get('id_producto', type=int)

        try:
            if accion == 'agregar' and id_producto:
                db.session.execute(
                    db.text("CALL sp_carrito_agregar(:id_usuario, :id_producto, :cantidad)"),
                    {
                        'id_usuario': id_usuario,
                        'id_producto': id_producto,
                        'cantidad': 1
                    }
                )
                db.session.commit()
                return redirect(url_for('venta.ventas'))

            if accion == 'quitar_unidad' and id_producto:
                db.session.execute(
                    db.text("CALL sp_carrito_quitar_unidad(:id_usuario, :id_producto)"),
                    {
                        'id_usuario': id_usuario,
                        'id_producto': id_producto
                    }
                )
                db.session.commit()
                return redirect(url_for('venta.ventas'))

            if accion == 'eliminar_producto' and id_producto:
                db.session.execute(
                    db.text("CALL sp_carrito_eliminar_producto(:id_usuario, :id_producto)"),
                    {
                        'id_usuario': id_usuario,
                        'id_producto': id_producto
                    }
                )
                db.session.commit()
                
                # Opcional: Registrar cuando se elimina un producto entero del carrito (suele ser útil por seguridad)
                audit.log_action(
                    module_name="logs_ventas",
                    action="Producto eliminado del carrito",
                    details={"email_cajero": email_usuario, "id_producto": id_producto},
                    level="INFO"
                )
                return redirect(url_for('venta.ventas'))

            if accion == 'completar':
                if create_form.validate():

                    result = db.session.execute(
                        db.text("""
                            CALL sp_venta_completar(
                                :id_usuario,
                                :id_metodo_pago,
                                :num_cuenta,
                                :monto_recibido
                            )
                        """),
                        {
                            'id_usuario': id_usuario,
                            'id_metodo_pago': create_form.metodo_pago.data,
                            'num_cuenta': create_form.numero_cuenta.data,
                            'monto_recibido': create_form.monto_recibido.data
                        }
                    )

                    # Obtenemos el id de la venta
                    row = result.fetchone()
                    id_venta = row[0] if row else None
                    db.session.commit()

                    metodo_nombre = next(
                        (
                            mp.nombre.lower()
                            for mp in lista_metodos
                            if str(mp.id_metodo_pago) == str(create_form.metodo_pago.data)
                        ),
                        ''
                    )

                    # --- REGISTRO DE AUDITORÍA: VENTA COMPLETADA ---
                    audit.log_action(
                        module_name="logs_ventas",
                        action="Venta Completada",
                        details={
                            "email_cajero": email_usuario, 
                            "id_venta": id_venta,
                            "metodo_pago": metodo_nombre,
                            "monto_recibido": create_form.monto_recibido.data
                        },
                        level="INFO"
                    )

                    if metodo_nombre == 'efectivo':
                        flash('Caja abierta. Efectivo registrado y cambio calculado correctamente.', 'success')
                    else:
                        flash('Cobro con tarjeta procesado correctamente.', 'success')

                    # Guardamos el id temporalmente
                    session['ticket_a_imprimir'] = id_venta

                    # Redirigimos a la pagina de ventas
                    return redirect(url_for('venta.ventas'))

        except (OperationalError, DBAPIError) as e:
            db.session.rollback()

            mensaje_usuario = 'Ocurrio un error al procesar la operación'

            try:
                codigo_mysql = e.orig.args[0]
                mensaje_mysql = e.orig.args[1]

                if codigo_mysql == 1644:
                    mensaje_usuario = mensaje_mysql
            except Exception:
                pass

            # --- REGISTRO DE AUDITORÍA: ERROR EN VENTA ---
            audit.log_action(
                module_name="logs_ventas",
                action="Error al procesar venta",
                details={"email_cajero": email_usuario, "error": mensaje_usuario},
                level="ERROR"
            )

            flash(mensaje_usuario, 'error')
            return redirect(url_for('venta.ventas'))    

    productos_venta = db.session.execute(
        db.text("""
            SELECT *
            FROM vw_productos_ventas
            WHERE activo = 1
            ORDER BY nombre
        """)
    ).mappings().all()

    carrito = db.session.execute(
        db.text("""
            SELECT *
            FROM vw_carrito_detalle
            WHERE id_usuario = :id_usuario
            ORDER BY nombre
        """),
        {'id_usuario': id_usuario}
    ).mappings().all()

    resumen = db.session.execute(
        db.text("""
            SELECT *
            FROM vw_carrito_resumen
            WHERE id_usuario = :id_usuario
            LIMIT 1
        """),
        {'id_usuario': id_usuario}
    ).mappings().first()

    if resumen is None:
        resumen = {
            'subtotal': 0.00,
            'descuento': 0.00,
            'total': 0.00,
            'total_piezas': 0
        }
    
    # Extraemos el id de la sesion del ticket de la venta y al final queremos que se borre
    # Automaticamente
    ticket_a_imprimir = session.pop('ticket_a_imprimir', None)
    return render_template('ventas/ventas.html', form=create_form, id_tarjeta=id_tarjeta, id_efectivo=id_efectivo, productos=productos_venta, carrito=carrito, resumen=resumen, ticket_a_imprimir = ticket_a_imprimir)

@venta.route('/ticket/<int:id_venta>')
@login_required
@roles_accepted('Cajero', 'cajero', 'Gerente', 'gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def ver_ticket(id_venta):
    cabecera = db.session.execute(
        db.text("SELECT * FROM vw_ticket_cabecera WHERE id_venta = :id"), 
        {'id': id_venta}
    ).mappings().first()
    
    detalles = db.session.execute(
        db.text("SELECT * FROM vw_ticket_detalle WHERE id_venta = :id"), 
        {'id': id_venta}
    ).mappings().all()

    if not cabecera:
        flash('Ticket no encontrado.', 'error')
        return redirect(url_for('venta.ventas'))

    return render_template('ventas/ticket_print.html', cabecera=cabecera, detalles=detalles)

@venta.route('/historial', methods=['GET', 'POST'])
@login_required
@roles_accepted('Cajero', 'cajero', 'Gerente', 'gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def historial():
    create_form = forms.FiltroFechaForm(request.args)

    if create_form.validate() and create_form.fecha.data:
        fecha_filtro = create_form.fecha.data
        query = db.text('SELECT * FROM vw_historial_caja WHERE DATE(fecha_movimiento) = :fecha ORDER BY fecha_movimiento DESC')
        movimientos = db.session.execute(query, {'fecha': fecha_filtro}).mappings().all()
    else:
        movimientos = db.session.execute(
            db.text('SELECT * FROM vw_historial_caja ORDER BY fecha_movimiento DESC LIMIT 100')
        ).mappings().all()

    return render_template('ventas/historial.html', movimientos = movimientos, form = create_form)

@venta.route('/CorteCaja', methods=['GET', 'POST'])
@login_required
@roles_accepted('Cajero', 'cajero', 'Gerente', 'gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def corte_caja():
    form = forms.Form()
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    fecha_vista = datetime.now().strftime('%d/%m/%Y')
    id_cajero = current_user.id_usuario 
    email_usuario = current_user.email # Email para auditoría

    if request.method == 'POST':
        try:
            connection = db.engine.raw_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            cursor.callproc('sp_guardar_corte_caja', [fecha_hoy, id_cajero])
            connection.commit() 
            
            rs_retiro = cursor.fetchone()
            monto_retirado = float(rs_retiro['monto_retirado']) if rs_retiro else 0.0
            
            # --- REGISTRO DE AUDITORÍA: CORTE DE CAJA EXITOSO ---
            audit.log_action(
                module_name="logs_ventas",
                action="Corte de Caja Realizado",
                details={"email_cajero": email_usuario, "monto_retirado": monto_retirado},
                level="INFO"
            )

            if monto_retirado > 0:
                flash(f'Corte de caja realizado. Se retiró ${monto_retirado:.2f} en efectivo.', 'success')
            else:
                flash('Corte realizado. No hubo efectivo que retirar el día de hoy.', 'info')
                
        except Exception as e:
            if 'connection' in locals():
                connection.rollback()
            
            mensaje_error = str(e)
            if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1644:
                mensaje_error = e.args[1]
                flash(f'{mensaje_error}', 'error')
            else:
                print(f'Error técnico detectado: {e}')
                flash('Hubó un error interno, que se comunique con el técnico.', 'error')

            # --- REGISTRO DE AUDITORÍA: ERROR EN CORTE DE CAJA ---
            audit.log_action(
                module_name="logs_ventas",
                action="Error en Corte de Caja",
                details={"email_cajero": email_usuario, "error": mensaje_error},
                level="ERROR"
            )

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
            
        return redirect(url_for('venta.corte_caja'))

    resumen = {
        'total_ventas': 0, 'total_efectivo': 0.0,
        'total_tarjeta': 0.0, 'transacciones_tarjeta': 0,
        'total_ingresos': 0.0 
    }
    detalle = []

    try:
        connection = db.engine.raw_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.callproc('sp_resumen_corte_caja', [fecha_hoy, id_cajero])
        rs1 = cursor.fetchone()
        if rs1 and rs1.get('total_ventas') is not None:
            resumen = rs1
        cursor.nextset()
        detalle = cursor.fetchall()
    except Exception as e:
        print(f'Error al visualizar datos: {e}') 
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

    return render_template('ventas/corte_caja.html', resumen=resumen, detalle=detalle, fecha_vista=fecha_vista, form=form)

@venta.route('/salidaCaja', methods=['GET', 'POST'])
@login_required
@roles_accepted('Cajero', 'cajero', 'Gerente', 'gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def salida_caja():
    create_form = forms.SalidaEfectivoForm(request.form)
    motivo = create_form.motivo.data
    monto = create_form.monto.data
    email_usuario = current_user.email # Email para auditoría

    if request.method == 'POST' and create_form.validate():
        id_cajero = current_user.id_usuario

        try:
            connection = db.engine.raw_connection()
            cursor = connection.cursor()

            cursor.callproc('sp_registrar_salida_efectivo', [id_cajero, monto, motivo])
            connection.commit()

            # --- REGISTRO DE AUDITORÍA: SALIDA DE EFECTIVO ---
            audit.log_action(
                module_name="logs_ventas",
                action="Salida de Efectivo Registrada",
                details={"email_cajero": email_usuario, "monto": monto, "motivo": motivo},
                level="INFO"
            )

            flash('Salida registrada correctamente', 'success')
            return redirect(url_for('venta.salida_caja'))
        
        except Exception as e:
            if 'connection' in locals():
                connection.rollback()

            mensaje_error = str(e)
            if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1644:
                mensaje_error = e.args[1]
                flash(f'{mensaje_error}', 'error')
            else:
                print(f'Error tecnico al registrar salida: {e}')
                flash('Hubo un error interno, comunicate con el técnico', 'error')

            # --- REGISTRO DE AUDITORÍA: ERROR EN SALIDA DE EFECTIVO ---
            audit.log_action(
                module_name="logs_ventas",
                action="Error al registrar Salida de Efectivo",
                details={"email_cajero": email_usuario, "error": mensaje_error},
                level="ERROR"
            )

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    salidas_hoy = db.session.execute(
        db.text('SELECT * FROM vw_salidas_efectivo WHERE DATE(fecha_hora) = CURRENT_DATE()')
    ).mappings().all()

    total_salidas_monto = sum(salida['monto'] for salida in salidas_hoy)

    return render_template('ventas/salidas_efectivo.html', form = create_form, salidas = salidas_hoy, total_hoy = total_salidas_monto)

@venta.route('/solicitudProduccionVenta', methods=['GET', 'POST'])
@login_required
@roles_accepted('Cajero', 'cajero', 'Gerente', 'gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def solicitud_produccion_venta():
    create_form = forms.SolicitudProduccionVentasForm(request.form)
    email_usuario = current_user.email # Email para auditoría

    if request.method == 'POST' and create_form.validate():
        id_producto = create_form.id_producto.data
        cantidad = create_form.cantidad.data
        id_usuario = current_user.id_usuario

        try:
            connection = db.engine.raw_connection()
            cursor = connection.cursor()

            cursor.callproc('sp_registrar_solicitud_produccion', [id_usuario, id_producto, cantidad])
            connection.commit()

            # --- REGISTRO DE AUDITORÍA: SOLICITUD DE PRODUCCIÓN ---
            audit.log_action(
                module_name="logs_ventas",
                action="Solicitud de Producción desde Caja",
                details={"email_cajero": email_usuario, "id_producto": id_producto, "cantidad": cantidad},
                level="INFO"
            )

            flash('Solicitud de producción enviada con éxito', 'success')
            return redirect(url_for('venta.solicitud_produccion_venta'))
        
        except Exception as e:
            if 'connection' in locals():
                connection.rollback()
            
            mensaje_error = str(e)
            if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1644:
                mensaje_error = e.args[1]
                flash(f'{mensaje_error}', 'error')
            else:
                print(f'Error tecnico al solicitar produccion: {e}')
                flash('Hubo un error interno, comunicate con el técnico', 'error')

            # --- REGISTRO DE AUDITORÍA: ERROR EN SOLICITUD DE PRODUCCIÓN ---
            audit.log_action(
                module_name="logs_ventas",
                action="Error al solicitar producción",
                details={"email_cajero": email_usuario, "error": mensaje_error},
                level="ERROR"
            )

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    productos = db.session.execute(
        db.text('SELECT * FROM vw_productos_produccion')
    ).mappings().all()

    return render_template('ventas/solicitud_produccion_venta.html', form = create_form, productos = productos)


@venta.route('/utilidad_diaria', methods=['GET', 'POST'])
@login_required
@roles_accepted('Gerente', 'gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def utilidad_diaria():
    form = forms.FiltroFechaForm(request.args)

    if form.validate() and form.fecha.data:
        fecha_consulta = form.fecha.data
    else:
        fecha_consulta = datetime.now().date()

    fecha_vista = fecha_consulta.strftime('%d/%m/%Y')

    datos_hoy = db.session.execute(
        db.text('SELECT * FROM vw_utilidad_diaria WHERE fecha = :fecha'),
        {'fecha': fecha_consulta}
    ).mappings().first()

    estadisticas = {
        'transacciones_ventas': 0,
        'total_ventas': 0.0,
        'costo_produccion': 0.0,
        'registros_salidas': 0,
        'total_salidas': 0.0,
        'margen_utilidad': 0.0
    }

    if datos_hoy:
        ventas = float(datos_hoy['total_ventas'] or 0)
        costos = float(datos_hoy['costo_produccion'] or 0)
        salidas = float(datos_hoy['total_salidas'] or 0)

        estadisticas['transacciones_ventas'] = datos_hoy['transacciones_ventas'] or 0
        estadisticas['total_ventas'] = ventas
        estadisticas['costo_produccion'] = costos
        estadisticas['registros_salidas'] = datos_hoy['registros_salidas'] or 0
        estadisticas['total_salidas'] = salidas

        utilidad_neta = ventas - costos - salidas

        if ventas > 0:
            estadisticas['margen_utilidad'] = (utilidad_neta / ventas) * 100

    return render_template('ventas/utilidad_diaria_venta.html', estadisticas=estadisticas, fecha_vista=fecha_vista, form=form)