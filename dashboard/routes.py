from flask import Blueprint, render_template, request, url_for, redirect
from models import db
from sqlalchemy import text
from datetime import datetime, timedelta

from . import dashboard

@dashboard.route('/dashboard')
def index():
    try:
        # 1. Ventas y Tickets de HOY
        resumen_hoy = db.session.execute(text("""
            SELECT 
                COALESCE(SUM(total), 0) as ventas_total,
                COUNT(id_venta) as tickets_total
            FROM ventas 
            WHERE DATE(fecha_venta) = CURDATE()
            AND estado_venta = 'Pagado'
        """)).fetchone()

        ventas_hoy = float(resumen_hoy[0])
        tickets_hoy = resumen_hoy[1]
        ganancia_hoy = ventas_hoy * 0.40 # Estimación del 40% de margen base

        # 2. Ranking de Productos (Top 3)
        ranking_productos = db.session.execute(text("""
            SELECT 
                p.nombre,
                c.nombre as categoria,
                SUM(dv.cantidad) as total_cantidad
            FROM detalle_ventas dv
            JOIN productos p ON dv.id_producto = p.id_producto
            JOIN categorias c ON p.id_categoria = c.id_categoria
            GROUP BY p.id_producto, p.nombre, c.nombre
            ORDER BY total_cantidad DESC
            LIMIT 3
        """)).fetchall()

        # 3. Datos para la Gráfica (Últimos 7 días)
        ventas_semanales = db.session.execute(text("""
            SELECT 
                DATE(fecha_venta) as fecha,
                SUM(total) as total
            FROM ventas
            WHERE fecha_venta >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            AND estado_venta = 'Pagado'
            GROUP BY DATE(fecha_venta)
            ORDER BY fecha ASC
        """)).fetchall()

        # Formatear datos para Chart.js
        chart_labels = [v[0].strftime('%d %b') for v in ventas_semanales]
        chart_data = [float(v[1]) for v in ventas_semanales]

        db.session.commit()

        return render_template('dashboard/index.html', 
                             ventas_hoy=ventas_hoy,
                             tickets_hoy=tickets_hoy,
                             ganancia_hoy=ganancia_hoy,
                             ranking=ranking_productos,
                             chart_labels=chart_labels,
                             chart_data=chart_data)

    except Exception as e:
        db.session.rollback()
        print(f"Error en dashboard: {str(e)}")
        return render_template('dashboard/index.html', 
                             ventas_hoy=0, 
                             tickets_hoy=0, 
                             ganancia_hoy=0, 
                             ranking=[],
                             chart_labels=[],
                             chart_data=[])
