from flask import render_template, request, url_for, flash, redirect
from . import venta
from sqlalchemy.exc import OperationalError, DBAPIError
from models import db
from models import Venta, DetalleVenta, MetodoPago
from extensions import limiter
import forms
import json, uuid
from sanitizador import Sanitizador
from flask_security import login_required, current_user
from flask_security.decorators import roles_required


@venta.route('/ventas', methods=['GET', 'POST'])
@login_required
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

    if request.method == 'POST':
        # create_form.id_tarjeta = id_tarjeta
        # create_form.id_efectivo = id_efectivo
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
                return redirect(url_for('venta.ventas'))

            if accion == 'completar':
                if create_form.validate():

                    db.session.execute(
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
                    db.session.commit()

                    metodo_nombre = next(
                        (
                            mp.nombre.lower()
                            for mp in lista_metodos
                            if str(mp.id_metodo_pago) == str(create_form.metodo_pago.data)
                        ),
                        ''
                    )

                    if metodo_nombre == 'efectivo':
                        flash('Caja abierta. Efectivo registrado y cambio calculado correctamente.', 'success')
                    else:
                        flash('Cobro con tarjeta procesado correctamente.', 'success')

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

    return render_template('ventas/ventas.html', form=create_form, id_tarjeta=id_tarjeta, id_efectivo=id_efectivo, productos=productos_venta, carrito=carrito, resumen=resumen)