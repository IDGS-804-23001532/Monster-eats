from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import Compra, Proveedor, Insumo, UnidadMedida, DetalleCompra, db
from . import compras
from sqlalchemy import text
import json
from flask_login import current_user
from forms import CompraForm
from audit_logger import audit
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted

@compras.route('/compras')
@login_required
@roles_accepted('Gerente', 'gerente')
def index():
    # Busqueda por proveedor
    search_query = request.args.get('search_query', '')
    if search_query:
        compras_list = Compra.query.join(Proveedor).filter(
            Proveedor.nombre_empresa.ilike(f'%{search_query}%')
        ).order_by(Compra.fecha_compra.desc()).all()
    else:
        compras_list = Compra.query.order_by(Compra.fecha_compra.desc()).all()
    
    # Formulario para validaciones macro
    form = CompraForm()
    # Obtener proveedores, insumos y unidades de medida
    proveedores = Proveedor.query.filter_by(activo=True).all()
    form.id_proveedor.choices = [(0, '-- Seleccionar proveedor --')] + [(p.id_proveedor, p.nombre_empresa) for p in proveedores]
    
    insumos_list = Insumo.query.filter_by(activo=True).all()
    unidades_medida = UnidadMedida.query.all()
    
    # Ver detalle de una compra específica
    detalle_compra = None
    show_modal = None
    cancel_compra = None
    
    ver_id = request.args.get('ver')
    if ver_id:
        detalle_compra = Compra.query.get(ver_id)
        if detalle_compra:
            show_modal = 'verDetalleModal'
    
    # Cancelar compra (GET abre el modal de confirmación)
    cancelar_id = request.args.get('cancelar')
    if cancelar_id:
        cancel_compra = Compra.query.get(cancelar_id)
        if cancel_compra:
            show_modal = 'cancelarCompraModal'
    
    # Historial de compras (GET abre el modal)
    historial_compras = None
    if request.args.get('historial'):
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM v_historial_compras ORDER BY fecha_compra DESC")
        columnas = [desc[0] for desc in cursor.description]
        historial_compras = [dict(zip(columnas, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        show_modal = 'historialComprasModal'
    
    return render_template('compras/index.html',
                         compras=compras_list,
                         search_query=search_query,
                         proveedores=proveedores,
                         form=form,
                         insumos=insumos_list,
                         unidades_medida=unidades_medida,
                         detalle_compra=detalle_compra,
                         cancel_compra=cancel_compra,
                         historial_compras=historial_compras,
                         show_modal=show_modal)

@compras.route('/limpiar_busqueda_compras')
def limpiar_busqueda():
    return redirect(url_for('compras.index'))


@compras.route('/nueva_compra', methods=['POST'])
def nueva_compra():
    form = CompraForm(request.form)
    # Re-poblar opciones para validación
    proveedores = Proveedor.query.filter_by(activo=True).all()
    form.id_proveedor.choices = [(0, '-- Seleccionar proveedor --')] + [(p.id_proveedor, p.nombre_empresa) for p in proveedores]

    if not form.validate():
        # Si falla, recargamos la página con el modal abierto y errores
        compras_list = Compra.query.order_by(Compra.fecha_compra.desc()).all()
        insumos_list = Insumo.query.filter_by(activo=True).all()
        unidades_medida = UnidadMedida.query.all()
        
        flash('Por favor corrige los errores del formulario', 'error')
        return render_template('compras/index.html',
                             compras=compras_list,
                             search_query='',
                             proveedores=proveedores,
                             form=form,
                             insumos=insumos_list,
                             unidades_medida=unidades_medida,
                             show_modal='nuevaCompraModal')

    try:
        id_proveedor = form.id_proveedor.data
        id_usuario = current_user.id_usuario
        
        # Toma todas las listas del formulario
        insumos_ids = request.form.getlist('insumo_id[]')
        cantidades = request.form.getlist('cantidad[]')
        costos = request.form.getlist('costo_unit[]')
        unidades = request.form.getlist('unidad_id[]')
        caducidades = request.form.getlist('caducidad[]')
        
        # Armar el JSON que espera el SP
        detalles = []
        for i in range(len(insumos_ids)):
            if insumos_ids[i] and cantidades[i] and costos[i]:
                cant = float(cantidades[i])
                cost = float(costos[i])
                
                # Validación backend estricta anti-negativos
                if cant <= 0 or cost < 0:
                    compras_list = Compra.query.order_by(Compra.fecha_compra.desc()).all()
                    insumos_list = Insumo.query.filter_by(activo=True).all()
                    unidades_medida = UnidadMedida.query.all()
                    flash('Alerta de seguridad: Las cantidades deben ser mayores a 0 y los costos no pueden ser negativos.', 'error')
                    return render_template('compras/index.html', compras=compras_list, search_query='', proveedores=proveedores, form=form, insumos=insumos_list, unidades_medida=unidades_medida, show_modal='nuevaCompraModal')
                
                # Verificamos que la caducidad no venga vacía
                if not caducidades[i] or caducidades[i].strip() == '':
                    compras_list = Compra.query.order_by(Compra.fecha_compra.desc()).all()
                    insumos_list = Insumo.query.filter_by(activo=True).all()
                    unidades_medida = UnidadMedida.query.all()
                    form.id_proveedor.errors.append('¡Aviso!: La Fecha de Caducidad es obligatoria para todos los insumos de la lista.')
                    flash('Error: Falta asignar la fecha de caducidad en uno o más insumos.', 'error')
                    return render_template('compras/index.html', compras=compras_list, search_query='', proveedores=proveedores, form=form, insumos=insumos_list, unidades_medida=unidades_medida, show_modal='nuevaCompraModal')
                
                caducidad_val = caducidades[i]
                
                detalles.append({
                    'id_insumo': int(insumos_ids[i]),
                    'cantidad': cant,
                    'id_unidad': int(unidades[i]),
                    'costo': cost,
                    'caducidad': caducidad_val
                })
        
        if not detalles:
            compras_list = Compra.query.order_by(Compra.fecha_compra.desc()).all()
            insumos_list = Insumo.query.filter_by(activo=True).all()
            unidades_medida = UnidadMedida.query.all()
            
            # Inyectamos el error directamente en el WTForm para que el macro lo dibuje en letras rojas
            form.id_proveedor.errors.append('¡Aviso!: Llena todas las celdas de los insumos (Cantidad, Costo, Unidad, Caducidad) o elimina las líneas vacías.')
            flash('Faltan datos de los insumos o no agregaste ninguno', 'error')
            return render_template('compras/index.html',
                                 compras=compras_list,
                                 search_query='',
                                 proveedores=proveedores,
                                 form=form,
                                 insumos=insumos_list,
                                 unidades_medida=unidades_medida,
                                 show_modal='nuevaCompraModal')
        
        detalles_json = json.dumps(detalles)
        
        # Llamar al procedimiento almacenado
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_registrar_compra', [id_proveedor, id_usuario, detalles_json])
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Compra registrada correctamente', 'success')
        
        # --- REGISTRO DE AUDITORÍA MONGO ---
        audit.log_action("Compras", "NUEVA COMPRA", details={
            "id_proveedor": id_proveedor,
            "articulos": len(detalles)
        })
    except Exception as e:
        audit.log_action("Compras", "ERROR NUEVA COMPRA", details={
            "error": str(e),
            "usuario": current_user.email
        })
        flash(f'Error al registrar la compra: {str(e)}', 'error')
    
    return redirect(url_for('compras.index'))


@compras.route('/cancelar_compra', methods=['POST'])
def cancelar_compra():
    try:
        id_compra = int(request.form.get('id_compra'))
        id_usuario = current_user.id_usuario
        
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_cancelar_compra', [id_compra, id_usuario])
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Compra cancelada correctamente', 'success')
        
        # --- REGISTRO DE AUDITORÍA MONGO ---
        audit.log_action("Compras", "CANCELACIÓN", details={
            "id_compra": id_compra
        })
    except Exception as e:
        error_msg = str(e)
        
        # Auditoría del intento de cancelación fallido
        audit.log_action("Compras", "FALLO AL CANCELAR", details={
            "id_compra_intentada": request.form.get('id_compra'),
            "razon": error_msg,
            "usuario": current_user.email
        })
        
        # Limpiamos el texto crudo del error para mostrar mensajes elegantes
        if 'La compra no existe' in error_msg:
            flash('Error: La compra seleccionada no existe.', 'error')
        elif 'La compra ya esta cancelada' in error_msg:
            flash('Aviso: Esta compra ya había sido cancelada previamente.', 'error')
        elif 'el lote ya fue consumido' in error_msg:
            flash('Cancelación rechazada: Uno o más insumos adquiridos en esta compra ya comenzaron a utilizarse en producción.', 'error')
        elif 'cannot be null' in error_msg:
            flash('Error de Integridad: Hay registros con cantidades nulas en esta compra o lote. Verifica los datos en la base de datos.', 'error')
        else:
            flash(f'Error al cancelar la compra: {error_msg}', 'error')
    
    return redirect(url_for('compras.index'))
