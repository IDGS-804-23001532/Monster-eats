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

        # Asegurar 7 días (llenar con ceros si falta alguno)
        from datetime import date, timedelta as _td
        today = date.today()
        last7 = [(today - _td(days=i)) for i in range(6, -1, -1)]
        vs_map = {r[0].date() if hasattr(r[0],'date') else r[0]: float(r[1]) for r in ventas_semanales}
        ventas_semanales_full = [(d, vs_map.get(d, 0.0)) for d in last7]

        # Formatear datos para Chart.js usando la serie completa de 7 días
        profit_margin = 0.40
        profit_series = [float(v) * profit_margin for _, v in ventas_semanales_full]
        # Métricas semanales
        weekly_total = sum(v[1] for v in ventas_semanales_full)
        weekly_profit_total = sum(float(v) * 0.40 for _, v in ventas_semanales_full)
        weekly_avg = weekly_profit_total / 7.0

        # Total semana anterior (7-13 días atrás)
        prev_start = today - _td(days=13)
        prev_end = today - _td(days=7)
        prev_row = db.session.execute(text("""
            SELECT COALESCE(SUM(total),0) FROM ventas
            WHERE DATE(fecha_venta) BETWEEN :start AND :end
            AND estado_venta = 'Pagado'
        """), {'start': prev_start, 'end': prev_end}).fetchone()
        prev_total = float(prev_row[0]) if prev_row and prev_row[0] is not None else 0.0
        week_growth = None
        prev_profit_total = prev_total * 0.40
        if prev_profit_total > 0:
            week_growth = (weekly_profit_total - prev_profit_total) / prev_profit_total * 100.0

        # Formatear datos para Chart.js usando la serie completa de 7 días (ganancias)
        chart_labels = [d.strftime('%d %b') for d, _ in ventas_semanales_full]
        chart_data = profit_series

        db.session.commit()

        return render_template('dashboard/index.html', 
                     ventas_hoy=ventas_hoy,
                     tickets_hoy=tickets_hoy,
                     ganancia_hoy=ganancia_hoy,
                     ranking=ranking_productos,
                     chart_labels=chart_labels,
                     chart_data=chart_data,
                     weekly_total=weekly_total,
                     weekly_profit_total=weekly_profit_total,
                     weekly_avg=weekly_avg,
                     week_growth=week_growth)

    except Exception as e:
        db.session.rollback()
        print(f"Error en dashboard: {str(e)}")
        return render_template('dashboard/index.html', 
                     ventas_hoy=0, 
                     tickets_hoy=0, 
                     ganancia_hoy=0, 
                     ranking=[],
                     chart_labels=[],
                     chart_data=[],
                     weekly_total=0,
                     weekly_profit_total=0,
                     weekly_avg=0,
                     week_growth=None)
