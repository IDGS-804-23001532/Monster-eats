from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, roles_accepted
from sqlalchemy import text
from . import recetas_bp
from models import db, Producto, Insumo

# --------------------------------------------------------------------------
# VISTA PRINCIPAL: LISTADO DE PRODUCTOS Y RENTABILIDAD
# --------------------------------------------------------------------------
@recetas_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente', 'cocinero')
def index():
    # Usamos la vista de rentabilidad para mostrar el resumen de costos
    query = text("SELECT * FROM v_rentabilidad_productos")
    productos_costos = db.session.execute(query).fetchall()
    return render_template('recetas/index.html', productos=productos_costos)

# --------------------------------------------------------------------------
# DETALLE DE RECETA: VER INGREDIENTES
# --------------------------------------------------------------------------
@recetas_bp.route('/detalle/<int:id_producto>')
@login_required
def detalle(id_producto):
    # Obtenemos info del producto
    producto = Producto.query.get_or_404(id_producto)
    
    # Consultamos la vista de detalle de recetas
    query = text("SELECT * FROM v_detalle_recetas WHERE id_producto = :id")
    ingredientes = db.session.execute(query, {"id": id_producto}).fetchall()
    
    # Lista de insumos para el modal de "Agregar Ingrediente"
    insumos_disponibles = Insumo.query.filter_by(activo=True).all()
    
    return render_template('recetas/detalle.html', 
                           producto=producto, 
                           ingredientes=ingredientes, 
                           insumos=insumos_disponibles)

# --------------------------------------------------------------------------
# ACCIÓN: GUARDAR/ACTUALIZAR INGREDIENTE (USA STORED PROCEDURE)
# --------------------------------------------------------------------------
@recetas_bp.route('/guardar', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def guardar_ingrediente():
    id_producto = request.form.get('id_producto')
    id_insumo = request.form.get('id_insumo')
    cantidad = request.form.get('cantidad')

    try:
        # Llamamos al SP que definimos anteriormente
        db.session.execute(
            text("CALL sp_upsert_ingrediente_receta(:p_prod, :p_ins, :p_cant)"),
            {"p_prod": id_producto, "p_ins": id_insumo, "p_cant": cantidad}
        )
        db.session.commit()
        flash("Ingrediente actualizado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar: {str(e)}", "danger")

    return redirect(url_for('recetas.detalle', id_producto=id_producto))

# --------------------------------------------------------------------------
# ACCIÓN: ELIMINAR INGREDIENTE
# --------------------------------------------------------------------------
@recetas_bp.route('/eliminar/<int:id_prod>/<int:id_ins>')
@login_required
@roles_accepted('admin', 'gerente')
def eliminar_ingrediente(id_prod, id_ins):
    try:
        # Eliminación directa (puedes mover esto a un SP si prefieres)
        db.session.execute(
            text("DELETE FROM recetas WHERE id_producto = :p AND id_insumo = :i"),
            {"p": id_prod, "i": id_ins}
        )
        db.session.commit()
        flash("Ingrediente removido de la receta", "info")
    except Exception as e:
        db.session.rollback()
        flash("No se pudo eliminar el ingrediente", "danger")
        
    return redirect(url_for('recetas.detalle', id_producto=id_prod))

# --------------------------------------------------------------------------
# SIMULACIÓN DE PRODUCCIÓN (EXPLOSIÓN DE MATERIALES)
# --------------------------------------------------------------------------
@recetas_bp.route('/simular', methods=['POST'])
@login_required
def simular():
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad_simular')
    
    # Llamamos al SP de simulación
    query = text("CALL sp_simular_produccion(:id, :cant)")
    resultado = db.session.execute(query, {"id": id_producto, "cant": cantidad}).fetchall()
    
    producto = Producto.query.get(id_producto)
    
    return render_template('recetas/simulacion.html', 
                           simulacion=resultado, 
                           producto=producto, 
                           cantidad=cantidad)