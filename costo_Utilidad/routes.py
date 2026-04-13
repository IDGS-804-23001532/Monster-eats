from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from sqlalchemy import text
from flask_security import login_required, roles_accepted
from audit_logger import audit

costo_utilidad = Blueprint('costo_utilidad', __name__, url_prefix='/costo-utilidad')

@costo_utilidad.route('/')
@login_required
@roles_accepted('Gerente', 'gerente') # REGLA: Bloqueo por decorador (Gerente y gerente)
def principal():
    try:
        # Creará y guardará en la colección "logs_finanzas"
        audit.log_action(
            module_name="logs_finanzas",
            action="Visualización Reporte Financiero", 
            details={"info": "Acceso a tabla de Costos y Utilidades"}, # Agregado para prevenir errores en MongoDB
            level="WARNING"
        )
        
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
        # CORRECCIÓN: Buscamos en "Pagado" o "Completada", y filtramos solo a tipo 'Producto' para no confundir IDs de combos.
        query_rentable = text("""
            SELECT cu.nombre, (cu.utilidad * SUM(dv.cantidad)) AS utilidad_global
            FROM vw_costo_utilidad cu
            JOIN detalle_ventas dv ON cu.id_producto = dv.id_producto
            JOIN ventas v ON dv.id_venta = v.id_venta
            WHERE v.estado_venta IN ('Pagado', 'Completada') AND cu.tipo = 'Producto'
            GROUP BY cu.id_producto, cu.nombre, cu.utilidad
            ORDER BY utilidad_global DESC
            LIMIT 1
        """)
        producto_rentable = db.session.execute(query_rentable).mappings().first()

        # 4. Preparar el desglose de recetas para los Modales
        desglose_recetas = {}
        for item in resultados:
            if item['tipo'] == 'Combo':
                # CORRECCIÓN: Adaptado a la nueva estructura "detalle_combos"
                query_combo = text("""
                    SELECT p.nombre, (dc.cantidad * cp.costo_produccion) AS costo 
                    FROM detalle_combos dc
                    JOIN productos p ON dc.id_producto = p.id_producto
                    JOIN vw_costo_productos cp ON p.id_producto = cp.id_producto
                    WHERE dc.id_combo = :id_padre
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
            
            # Guardamos el desglose usando una clave combinada (Ej: "Producto_1" o "Combo_1") 
            # para evitar que el Producto #1 y el Combo #1 se sobreescriban entre sí.
            llave_unica = f"{item['tipo']}_{item['id_producto']}"
            desglose_recetas[llave_unica] = ingredientes

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

