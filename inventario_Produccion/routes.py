from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Producto, InventarioProducto
from flask_security import login_required, roles_accepted, current_user
from forms import AjusteStockForm  
from audit_logger import audit  

inventario_produccion = Blueprint('inventario_produccion', __name__, url_prefix='/inventario-produccion')

@inventario_produccion.route('/', methods=['GET', 'POST'])
@login_required
@roles_accepted('administrador', 'gerente', 'cocina', 'cocinero')
def principal():
    # Instanciamos el formulario de Flask-WTF
    form = AjusteStockForm()

    # ---------------------------------------------------------
    # LÓGICA POST: Si el usuario envió el formulario del modal
    # ---------------------------------------------------------
    if form.validate_on_submit():
        try:
            id_prod = form.id_producto.data
            cantidad_ajuste = form.cantidad.data  # Puede ser positivo (+5) o negativo (-2)
            motivo = form.motivo.data

            # Buscamos el registro de inventario actual
            inventario = InventarioProducto.query.filter_by(id_producto=id_prod).first()
            
            # Si no existía un registro previo, lo creamos desde cero
            if not inventario:
                inventario = InventarioProducto(id_producto=id_prod, stock_actual=0)
                db.session.add(inventario)
            
            # Aplicamos la suma algebraica (si ingresó -5, se restará. Si ingresó 10, se sumará)
            inventario.stock_actual += cantidad_ajuste

            db.session.commit()

            # Guardamos el movimiento en la bitácora de auditoría (MongoDB)
            audit.log_action(
                module_name="inventario_produccion", 
                action="Ajuste Manual de Stock", 
                details={
                    "id_producto": id_prod, 
                    "ajuste": cantidad_ajuste, 
                    "stock_resultante": inventario.stock_actual,
                    "motivo": motivo
                },
                level="INFO"
            )

            flash('¡Stock ajustado correctamente!', 'success')
            return redirect(url_for('inventario_produccion.principal'))

        except Exception as e:
            db.session.rollback()
            print(f"Error al ajustar stock en producción: {e}")
            flash('Error en la base de datos al guardar el ajuste.', 'error')
            
    elif request.method == 'POST':
        # Si el form se envió pero no pasó las validaciones de WTF
        flash('Error en los datos ingresados. Revisa el formulario.', 'error')

    # 1. Filtramos inteligentemente: Solo productos activos que NO son combos y NO se hacen al momento
    productos_lote = Producto.query.filter_by(
        activo=True, 
    ).all()
    
    # 2. Armamos las parejas (tuplas) que tu HTML necesita
    productos_stock = []
    for prod in productos_lote:
        inv = InventarioProducto.query.filter_by(id_producto=prod.id_producto).first()
        
        # Si el producto es nuevo y aún no tiene registro de stock, creamos un objeto temporal en 0
        # (Nota: No lo guardamos en la base de datos aún, solo es para que el HTML pueda pintarlo sin errores)
        if not inv:
            inv = InventarioProducto(id_producto=prod.id_producto, stock_actual=0)
            
        # Agregamos la pareja exacta (inv, prod) a la lista
        productos_stock.append((inv, prod))
    
    # Mandamos los datos al HTML, incluyendo el formulario para los modales
    return render_template(
        'inventario_Produccion/principal.html', 
        productos_stock=productos_stock, 
        form=form
    )
