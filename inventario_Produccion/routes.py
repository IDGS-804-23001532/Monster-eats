from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Producto, InventarioProducto, MovimientoInventarioProducto
from flask_security import login_required, roles_accepted, current_user
from forms import AjusteStockForm  
from audit_logger import audit  

inventario_produccion = Blueprint('inventario_produccion', __name__, url_prefix='/inventario-produccion')

@inventario_produccion.route('/', methods=['GET', 'POST'])
@login_required
@roles_accepted('administrador', 'gerente', 'cocina', 'cocinero')
def principal():
    form = AjusteStockForm()

    # ---------------------------------------------------------
    # LÓGICA POST: Procesamiento del Ajuste o Merma
    # ---------------------------------------------------------
    if form.validate_on_submit():
        try:
            id_prod = form.id_producto.data
            cantidad_ajuste = form.cantidad.data  # Ej: 5 (ingreso extra) o -2 (merma)
            motivo = form.motivo.data

            # 1. Buscamos o creamos el inventario
            inventario = InventarioProducto.query.filter_by(id_producto=id_prod).first()
            if not inventario:
                inventario = InventarioProducto(id_producto=id_prod, stock_actual=0)
                db.session.add(inventario)
            
            # Guardamos el stock anterior para el historial
            stock_anterior = inventario.stock_actual
            stock_nuevo = stock_anterior + cantidad_ajuste

            # 2. Validación de seguridad: Evitar stock negativo
            if stock_nuevo < 0:
                flash(f'Error: No puedes restar {abs(cantidad_ajuste)} porque solo hay {stock_anterior} en stock.', 'error')
                return redirect(url_for('inventario_produccion.principal'))

            # 3. Clasificar el tipo de movimiento para el historial SQL
            if cantidad_ajuste < 0:
                # Si el usuario escribe "merma", "caducado" o "dañado" en el motivo, lo clasificamos específicamente
                if any(palabra in motivo.lower() for palabra in ['merma', 'caducado', 'dañado', 'basura', 'accidente']):
                    tipo_mov = 'SALIDA_MERMA'
                else:
                    tipo_mov = 'AJUSTE_NEGATIVO'
            else:
                tipo_mov = 'AJUSTE_POSITIVO'

            # 4. Actualizamos el stock final
            inventario.stock_actual = stock_nuevo

            # 5. Registramos el movimiento en la tabla SQL (Crucial para reportes financieros)
            movimiento = MovimientoInventarioProducto(
                id_producto=id_prod,
                tipo_movimiento=tipo_mov,
                cantidad=abs(cantidad_ajuste), # Guardamos el valor absoluto (siempre positivo)
                stock_anterior=stock_anterior,
                stock_nuevo=stock_nuevo,
                origen='ajuste_manual',
                descripcion=motivo,
                id_usuario=current_user.id_usuario
            )
            db.session.add(movimiento)
            
            db.session.commit()

            # 6. Guardamos en bitácora NoSQL (Auditoría de seguridad)
            audit.log_action(
                module_name="inventario_produccion", 
                action=f"Ajuste de Stock ({tipo_mov})", 
                details={
                    "id_producto": id_prod, 
                    "ajuste": cantidad_ajuste, 
                    "stock_resultante": stock_nuevo,
                    "motivo": motivo,
                    "usuario": current_user.email
                },
                level="INFO"
            )

            flash(f'Stock actualizado correctamente. Nuevo total: {stock_nuevo}', 'success')
            return redirect(url_for('inventario_produccion.principal'))

        except Exception as e:
            db.session.rollback()
            print(f"Error al ajustar stock en producción: {e}")
            flash('Error en la base de datos al guardar el ajuste.', 'error')
            
    elif request.method == 'POST':
        flash('Error en los datos ingresados. Revisa el formulario.', 'error')
    # ---------------------------------------------------------
    # LÓGICA GET: Mostrar el tablero
    # ---------------------------------------------------------
    # Filtramos productos activos. 
    # Nota: Según tu DB, los combos están en su propia tabla, así que 'Producto' ya trae puros productos individuales.
    productos_lote = Producto.query.filter_by(activo=True).all()
    
    productos_stock = []
    for prod in productos_lote:
        inv = InventarioProducto.query.filter_by(id_producto=prod.id_producto).first()
        
        if not inv:
            inv = InventarioProducto(id_producto=prod.id_producto, stock_actual=0)
            
        productos_stock.append((inv, prod))
    
    return render_template(
        'inventario_Produccion/principal.html', 
        productos_stock=productos_stock, 
        form=form
    )
