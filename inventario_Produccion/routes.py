from flask import Blueprint, render_template
from models import db, InventarioProducto, Producto, Combo, MovimientoInventarioProducto
from flask import request, flash, redirect, url_for
from datetime import datetime
from forms import AjusteStockForm
#from flask_security import login_required

# Ajusta el nombre del blueprint a como lo tengas definido en tu __init__.py
inventario_produccion = Blueprint('inventario_produccion', __name__, url_prefix='/inventario-produccion')

@inventario_produccion.route('/', methods=['GET', 'POST'])
def principal():
    # Mantenemos la instancia para que el modal no marque error al renderizar
    form = AjusteStockForm() 
    
    # Procesamos el ajuste si la petición es POST
    if request.method == 'POST':
        # Obtenemos datos directamente del formulario (sin validación estricta de WTF)
        id_prod = request.form.get('id_producto')
        cantidad_raw = request.form.get('cantidad')
        motivo = request.form.get('motivo')
        
        try:
            cantidad_ajuste = int(cantidad_raw)
            inv = InventarioProducto.query.filter_by(id_producto=id_prod).first()
            
            if inv:
                stock_anterior = inv.stock_actual
                inv.stock_actual += cantidad_ajuste
                
                # Registro de movimiento (Auditoría básica con ID de usuario fijo)
                movimiento = MovimientoInventarioProducto(
                    id_producto=id_prod,
                    tipo_movimiento='AJUSTE_MANUAL',
                    cantidad=abs(cantidad_ajuste),
                    stock_anterior=stock_anterior,
                    stock_nuevo=inv.stock_actual,
                    motivo=motivo,
                    id_usuario=1, # ID fijo para evitar el uso de current_user
                    fecha_movimiento=datetime.now()
                )
                db.session.add(movimiento)
                db.session.commit()
                flash('Stock actualizado y movimiento registrado correctamente.', 'success')
            
            return redirect(url_for('inventario_produccion.principal'))
            
        except (ValueError, TypeError):
            flash('Error: La cantidad debe ser un número válido.', 'error')
            return redirect(url_for('inventario_produccion.principal'))

    # Consulta para mostrar la tabla (Regla RF09: Excluye combos)
    subquery_padres = db.session.query(Combo.id_producto_padre).distinct()
    productos_stock = db.session.query(InventarioProducto, Producto)\
        .join(Producto, InventarioProducto.id_producto == Producto.id_producto)\
        .filter(~Producto.id_producto.in_(subquery_padres))\
        .all()

    return render_template('inventario_Produccion/principal.html', 
                           productos_stock=productos_stock, 
                           form=form)

@inventario_produccion.route('/combos')
#@login_required
def combos_dinamicos():
    # 1. Buscamos todos los productos que actúan como "Padre" (que son combos)
    subquery_padres = db.session.query(Combo.id_producto_padre).distinct()
    combos_padres = db.session.query(Producto).filter(Producto.id_producto.in_(subquery_padres)).all()

    combos_data = []
    
    for padre in combos_padres:
        # 2. Por cada combo, buscamos qué productos "Hijos" incluye y su stock actual
        hijos_info = db.session.query(Combo, Producto, InventarioProducto)\
            .join(Producto, Combo.id_producto_hijo == Producto.id_producto)\
            .outerjoin(InventarioProducto, Producto.id_producto == InventarioProducto.id_producto)\
            .filter(Combo.id_producto_padre == padre.id_producto)\
            .all()
        
        # 3. Calculamos la disponibilidad real del combo (el ingrediente limitante)
        # Si un hijo no tiene registro en inventario, su stock es 0.
        stock_posible = []
        for hijo in hijos_info:
            stock_actual = hijo.InventarioProducto.stock_actual if hijo.InventarioProducto else 0
            cantidad_requerida = hijo.Combo.cantidad
            stock_posible.append(int(stock_actual // cantidad_requerida))
            
        stock_combo_final = min(stock_posible) if stock_posible else 0

        combos_data.append({
            'padre': padre,
            'hijos': hijos_info,
            'stock_disponible': stock_combo_final
        })

    return render_template('inventario_Produccion/combosDinamicos.html', combos_data=combos_data)

@inventario_produccion.route('/ajustar_stock', methods=['POST'])
def ajustar_stock():
    # Obtenemos los datos directamente del name del input en el HTML
    id_prod = request.form.get('id_producto')
    cantidad_ajuste = request.form.get('cantidad')
    motivo = request.form.get('motivo')

    try:
        # Convertimos a entero para la operación matemática
        cantidad_int = int(cantidad_ajuste)
        
        # Buscamos el registro en la tabla inventario_productos
        inv = InventarioProducto.query.filter_by(id_producto=id_prod).first()
        
        if inv:
            stock_anterior = inv.stock_actual
            inv.stock_actual += cantidad_int # Sumamos o restamos
            
            # Creamos el registro de movimiento (Auditoría básica)
            # Usamos id_usuario = 1 de forma fija
            movimiento = MovimientoInventarioProducto(
                id_producto=id_prod,
                tipo_movimiento='AJUSTE_MANUAL',
                cantidad=abs(cantidad_int),
                stock_anterior=stock_anterior,
                stock_nuevo=inv.stock_actual,
                motivo=motivo,
                id_usuario=1, # <--- ID fijo para evitar el error de current_user
                fecha_movimiento=datetime.now()
            )
            
            db.session.add(movimiento)
            db.session.commit()
            flash('Stock actualizado correctamente', 'success')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('inventario_produccion.principal'))