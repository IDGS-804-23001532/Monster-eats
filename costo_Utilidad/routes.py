from flask import Blueprint, render_template, flash, redirect, url_for
from models import db
from sqlalchemy import text
from flask_security import login_required, roles_accepted

costo_utilidad = Blueprint('costo_utilidad', __name__, url_prefix='/costo-utilidad')

@costo_utilidad.route('/')
@login_required
@roles_accepted('Gerente') # REGLA: Bloqueo estricto por decorador
def principal():
    try:
        # 1. Obtener la tabla principal de Costo y Utilidad
        query_principal = text("SELECT * FROM vw_costo_utilidad ORDER BY margen_ganancia ASC")
        resultados = db.session.execute(query_principal).mappings().fetchall()

        # 2. Calcular KPIs Superiores
        if resultados:
            margen_promedio = sum(item['margen_ganancia'] for item in resultados) / len(resultados)
            alertas_costos = sum(1 for item in resultados if item['margen_ganancia'] < 50)
            rentabilidad_general = sum(item['utilidad'] for item in resultados) / len(resultados) 
        else:
            margen_promedio = 0
            alertas_costos = 0
            rentabilidad_general = 0

        # 3. KPI: Producto más rentable (Cruza Ventas Pagadas x Utilidad Neta)
        query_rentable = text("""
            SELECT cu.nombre, (cu.utilidad * SUM(dv.cantidad)) AS utilidad_global
            FROM vw_costo_utilidad cu
            JOIN detalle_ventas dv ON cu.id_producto = dv.id_producto
            JOIN ventas v ON dv.id_venta = v.id_venta
            WHERE v.estado_venta = 'Pagado'
            GROUP BY cu.id_producto, cu.nombre, cu.utilidad
            ORDER BY utilidad_global DESC
            LIMIT 1
        """)
        producto_rentable = db.session.execute(query_rentable).mappings().first()

        # 4. Preparar el desglose de recetas para los Modales
        desglose_recetas = {}
        for item in resultados:
            if item['tipo'] == 'Combo':
                query_combo = text("""
                    SELECT p.nombre, (c.cantidad * cp.costo_produccion) AS costo 
                    FROM combos c
                    JOIN productos p ON c.id_producto_hijo = p.id_producto
                    JOIN vw_costo_productos cp ON p.id_producto = cp.id_producto
                    WHERE c.id_producto_padre = :id_padre
                """)
                ingredientes = db.session.execute(query_combo, {'id_padre': item['id_producto']}).mappings().fetchall()
            else:
                query_receta = text("""
                    SELECT i.nombre, (r.cantidad_requerida * i.costo_unitario) AS costo 
                    FROM recetas r
                    JOIN insumos i ON r.id_insumo = i.id_insumo
                    WHERE r.id_producto = :id_prod
                """)
                ingredientes = db.session.execute(query_receta, {'id_prod': item['id_producto']}).mappings().fetchall()
            
            desglose_recetas[item['id_producto']] = ingredientes

        return render_template('costo_Utilidad/principal.html', 
                               resultados=resultados,
                               margen_promedio=margen_promedio,
                               alertas_costos=alertas_costos,
                               rentabilidad_general=rentabilidad_general,
                               producto_rentable=producto_rentable,
                               desglose_recetas=desglose_recetas)
                               
    except Exception as e:
        print(f"Error en SQL: {e}")
        flash('Error al generar reporte financiero. Revisa las Vistas SQL.', 'error')
        return redirect(url_for('dashboard.index'))