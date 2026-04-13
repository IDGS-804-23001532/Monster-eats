from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Producto, InventarioProducto, MovimientoInventarioProducto
from flask_security import login_required, roles_accepted, current_user
from forms import AjusteStockForm  
from audit_logger import audit  
import csv
from io import StringIO
from flask import Response

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
            # Según el Enum de tu base de datos, todo ajuste desde aquí es "AJUSTE_MANUAL"
            tipo_mov = 'AJUSTE_MANUAL'

            # 4. Actualizamos el stock final
            inventario.stock_actual = stock_nuevo

            # 5. Registramos el movimiento en la tabla SQL
            movimiento = MovimientoInventarioProducto(
                id_producto=id_prod,
                tipo_movimiento=tipo_mov,
                cantidad=abs(cantidad_ajuste), # Valor absoluto (siempre positivo)
                stock_anterior=stock_anterior,
                stock_nuevo=stock_nuevo,
                motivo=motivo, # CORRECCIÓN: Se llama 'motivo', no 'descripcion'
                referencia_tabla='ajuste_inventario', # Usamos esto en vez del campo 'origen'
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
    # LÓGICA GET: Mostrar el tablero (CON BUSCADOR)
    # ---------------------------------------------------------
    
    # 1. Atrapamos el término de búsqueda de la URL (?q=...)
    search_query = request.args.get('q', '').strip()
    
    # 2. Iniciamos la consulta base (Solo activos)
    query = Producto.query.filter_by(activo=True)
    
    # 3. Si el usuario escribió algo en el buscador, encadenamos el filtro
    if search_query:
        query = query.filter(Producto.nombre.ilike(f"%{search_query}%"))
        
    # 4. Ejecutamos la consulta final filtrada
    productos_lote = query.all()
    
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

@inventario_produccion.route('/exportar-csv')
@login_required
@roles_accepted('administrador', 'gerente', 'cocina', 'cocinero')
def exportar_csv():
    # 1. Atrapamos la palabra de búsqueda para que el Excel coincida con la pantalla
    search_query = request.args.get('q', '').strip()
    
    query = Producto.query.filter_by(activo=True)
    if search_query:
        query = query.filter(Producto.nombre.ilike(f"%{search_query}%"))
        
    productos_lote = query.all()
    
    def generate():
        data = StringIO()
        # 2. Agregamos el BOM (Byte Order Mark) de UTF-8. 
        # Esto obliga a Microsoft Excel a leer correctamente los acentos (á, é, í) y la ñ.
        data.write('\ufeff')
        
        writer = csv.writer(data)
        
        # Cabeceras del Excel
        writer.writerow(('ID', 'Producto Terminado', 'Stock en Cocina', 'Precio Venta ($)'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        for prod in productos_lote:
            inv = InventarioProducto.query.filter_by(id_producto=prod.id_producto).first()
            stock_actual = inv.stock_actual if inv else 0
            
            writer.writerow((
                prod.id_producto,
                prod.nombre,
                stock_actual,
                f"{prod.precio_venta:.2f}"
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # 3. Aseguramos que el mimetype también especifique utf-8
    response = Response(generate(), mimetype='text/csv; charset=utf-8')
    
    # Nombre dinámico del archivo dependiendo de si hay búsqueda o no
    if search_query:
        filename = f"Inventario_Filtrado_{search_query}.csv"
    else:
        filename = "Inventario_Cocina_MonsterEats.csv"
        
    response.headers.set("Content-Disposition", "attachment", filename=filename)
    return response