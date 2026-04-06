# recetas/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Producto, Insumo, UnidadMedida
from sqlalchemy import text
import logging
from . import recetas_bp
import forms

logger = logging.getLogger(__name__)

@recetas_bp.route('/')
def index():
    search = request.args.get('search', '')
    try:
        query = text("CALL SP_Recetas_ObtenerTodos(:search)")
        recetas = db.session.execute(query, {'search': search}).fetchall()
        db.session.commit()  # Limpiar resultados del CALL
        
        return render_template('recetas/index.html', recetas=recetas, search=search)
    
    except Exception as e:
        logger.error(f"Error en index de recetas: {str(e)}")
        flash('Error al cargar las recetas', 'danger')
        return render_template('recetas/index.html', recetas=[])


@recetas_bp.route('/detalle/<int:id>')
def detalle(id):
    try:
        # 1. Obtener información del producto
        query_producto = text("""
            SELECT 
                p.id_producto,
                p.nombre AS producto,
                p.precio_venta,
                c.nombre AS categoria,
                p.activo,
                COALESCE(SUM(r.cantidad_requerida * i.costo_unitario), 0) AS costo_total
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN recetas r ON p.id_producto = r.id_producto
            LEFT JOIN insumos i ON r.id_insumo = i.id_insumo
            WHERE p.id_producto = :id
            GROUP BY p.id_producto, p.nombre, p.precio_venta, c.nombre, p.activo
        """)
        
        producto_result = db.session.execute(query_producto, {'id': id}).fetchone()
        db.session.commit()
        
        if not producto_result:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('recetas.index'))
        
        # Convertir a diccionario para fácil acceso
        producto = {
            'id_producto': producto_result[0],
            'producto': producto_result[1],
            'precio_venta': float(producto_result[2]),
            'categoria': producto_result[3],
            'activo': producto_result[4],
            'costo_total': float(producto_result[5])
        }
        
        # 2. Obtener insumos de la receta
        query_insumos = text("""
            SELECT 
                r.id_insumo,
                i.nombre AS insumo,
                r.cantidad_requerida,
                um.nombre AS unidad_medida,
                um.abreviatura,
                i.costo_unitario,
                ROUND(r.cantidad_requerida * i.costo_unitario, 2) AS costo_parcial
            FROM recetas r
            JOIN insumos i ON r.id_insumo = i.id_insumo
            JOIN unidades_medida um ON i.id_unidad_medida = um.id_unidad_medida
            WHERE r.id_producto = :id
            ORDER BY i.nombre
        """)
        
        insumos_result = db.session.execute(query_insumos, {'id': id}).fetchall()
        db.session.commit()
        
        # Convertir insumos a lista de diccionarios
        insumos = []
        for row in insumos_result:
            insumos.append({
                'id_insumo': row[0],
                'insumo': row[1],
                'cantidad_requerida': float(row[2]),
                'unidad_medida': row[3],
                'abreviatura': row[4],
                'costo_unitario': float(row[5]),
                'costo_parcial': float(row[6])
            })
        
        # 3. Obtener insumos disponibles para agregar
        query_disponibles = text("""
            SELECT 
                i.id_insumo,
                i.nombre,
                um.abreviatura,
                i.costo_unitario
            FROM insumos i
            JOIN unidades_medida um ON i.id_unidad_medida = um.id_unidad_medida
            WHERE i.activo = 1
            AND i.id_insumo NOT IN (
                SELECT id_insumo FROM recetas WHERE id_producto = :id
            )
            ORDER BY i.nombre
        """)
        
        disponibles_result = db.session.execute(query_disponibles, {'id': id}).fetchall()
        db.session.commit()
        
        # Crear formulario
        form = forms.RecetaInsumoForm()
        form.id_producto.data = id
        form.id_insumo.choices = [(row[0], f"{row[1]} ({row[2]}) - ${float(row[3]):.2f}") 
                                   for row in disponibles_result]
        
        return render_template('recetas/detalle.html', 
                             producto=producto, 
                             insumos=insumos,
                             form=form)
    
    except Exception as e:
        db.session.rollback()
        print(f"Error en detalle: {str(e)}")
        flash('Error al cargar el detalle de la receta', 'danger')
        return redirect(url_for('recetas.index'))    

@recetas_bp.route('/agregar_insumo', methods=['POST'])
def agregar_insumo():
    id_producto = request.form.get('id_producto', type=int)
    id_insumo = request.form.get('id_insumo', type=int)
    cantidad = request.form.get('cantidad_requerida', type=float)
    
    if not id_producto or not id_insumo or not cantidad:
        flash('Faltan datos requeridos', 'danger')
        return redirect(url_for('recetas.detalle', id=id_producto))
    
    try:
        # SQL directo para insertar o actualizar
        query = text("""
            INSERT INTO recetas (id_producto, id_insumo, cantidad_requerida)
            VALUES (:id_producto, :id_insumo, :cantidad)
            ON DUPLICATE KEY UPDATE cantidad_requerida = :cantidad
        """)
        db.session.execute(query, {
            'id_producto': id_producto,
            'id_insumo': id_insumo,
            'cantidad': cantidad
        })
        db.session.commit()
        
        flash('Insumo agregado correctamente a la receta', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al agregar insumo: {str(e)}")
        flash(f'Error al agregar insumo: {str(e)}', 'danger')
    
    return redirect(url_for('recetas.detalle', id=id_producto))

@recetas_bp.route('/eliminar_insumo/<int:id_producto>/<int:id_insumo>', methods=['POST'])
def eliminar_insumo(id_producto, id_insumo):
    try:
        query = text("DELETE FROM recetas WHERE id_producto = :id_producto AND id_insumo = :id_insumo")
        db.session.execute(query, {
            'id_producto': id_producto,
            'id_insumo': id_insumo
        })
        db.session.commit()
        
        flash('Insumo eliminado de la receta', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar insumo: {str(e)}")
        flash(f'Error al eliminar insumo: {str(e)}', 'danger')
    
    return redirect(url_for('recetas.detalle', id=id_producto))

@recetas_bp.route('/limpiar/<int:id_producto>', methods=['POST'])
def limpiar(id_producto):
    try:
        query = text("CALL SP_Recetas_Limpiar(:id_producto)")
        db.session.execute(query, {'id_producto': id_producto})
        db.session.commit()
        
        flash('Receta limpiada completamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al limpiar receta: {str(e)}")
        flash(f'Error al limpiar receta: {str(e)}', 'danger')
    
    return redirect(url_for('recetas.detalle', id=id_producto))


@recetas_bp.route('/insumos_disponibles')
def insumos_disponibles():
    product_id = request.args.get('product_id', type=int)
    search = request.args.get('search', '')
    
    try:
        query = text("CALL SP_Recetas_InsumosDisponibles(:id_producto, :search)")
        insumos = db.session.execute(query, {
            'id_producto': product_id,
            'search': search
        }).fetchall()
        db.session.commit()
        
        return {'insumos': [{'id': i.id_insumo, 'nombre': i.nombre, 'unidad': i.abreviatura} 
                           for i in insumos]}
    
    except Exception as e:
        logger.error(f"Error al buscar insumos: {str(e)}")
        return {'insumos': []}