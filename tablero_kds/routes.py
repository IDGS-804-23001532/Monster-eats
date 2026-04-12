from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
from audit_logger import audit
import traceback

# Creamos el Blueprint exclusivo para el Kitchen Display System (KDS)
tablero_kds = Blueprint('tablero_kds', __name__, url_prefix='/kds')

# ==========================================================================
# PANTALLA PRINCIPAL DEL TABLERO
# ==========================================================================
@tablero_kds.route('/')
@login_required
@roles_accepted('Cocina', 'Gerente', 'gerente', 'cocina') 
def principal():
    try:
        query = text("SELECT * FROM vw_kds_cocina")
        resultados = db.session.execute(query).mappings().fetchall()
        comandas = [dict(row) for row in resultados]

        return render_template('tablero_kds/principal.html', comandas=comandas)
    
    except Exception as e:
        print("\n ERROR GRAVE EN EL KDS:")
        traceback.print_exc()  # <--- ESTO IMPRIME LA LÍNEA EXACTA DEL ERROR
        flash(f'Error técnico: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

# ==========================================================================
# DESPACHAR PLATILLO (MARCAR COMO LISTO)
# ==========================================================================
@tablero_kds.route('/marcar-listo/<int:id_detalle>', methods=['POST'])
@login_required
@roles_accepted('Cocina', 'Gerente', 'gerente', 'cocina', 'cocinero')
def marcar_listo(id_detalle):
    try:
        # Llamamos al Procedimiento Almacenado "Mágico"
        # 1. Cambia estado a 'Listo'
        # 2. Lee la receta
        # 3. Descuenta lotes de insumos (FIFO)
        db.session.execute(
            text("CALL SP_KDS_MarcarListo(:id_detalle, :id_usuario)"),
            {
                'id_detalle': id_detalle,
                'id_usuario': current_user.id_usuario
            }
        )
        db.session.commit()
        
        # Registro en la bitácora de auditoría (MongoDB)
        audit.log_action(
            module_name="logs_kds", 
            action="Platillo Terminado", 
            details={"id_detalle_venta": id_detalle},
            level="INFO"
        )
        
        flash('¡Platillo marcado como LISTO! El Cajero ya puede entregarlo.', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error en KDS al despachar: {e}")
        
        # Manejo de errores amigable (Si el SP detecta que no hay ingredientes)
        error_msg = str(e)
        if 'Stock de materia prima insuficiente' in error_msg:
            flash('Error: No hay materia prima suficiente en inventario para preparar este platillo.', 'error')
        else:
            flash('Hubo un error al intentar despachar el platillo.', 'error')
            
    return redirect(url_for('tablero_kds.principal'))