from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
from audit_logger import audit
import traceback

tablero_kds = Blueprint('tablero_kds', __name__, url_prefix='/kds')

@tablero_kds.route('/')
@login_required
@roles_accepted('administrador', 'gerente', 'cocina', 'cocinero')
def principal():
    try:
        # Leemos nuestra nueva vista mágica unificada
        query = text("SELECT * FROM vw_kds_unificado")
        resultados = db.session.execute(query).mappings().fetchall()
        comandas = [dict(row) for row in resultados]

        return render_template('tablero_kds/principal.html', comandas=comandas)
    
    except Exception as e:
        print("\n ERROR EN EL KDS:")
        traceback.print_exc()
        flash(f'Error técnico: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))


@tablero_kds.route('/marcar-listo', methods=['POST'])
@login_required
@roles_accepted('administrador', 'gerente', 'cocina', 'cocinero')
def marcar_listo():
    # recibimos el ID y el tipo de origen desde el formulario
    id_origen = request.form.get('id_origen')
    origen = request.form.get('origen')
    try:
        # Llamamos al nuevo Stored Procedure Mágico Unificado
        db.session.execute(
            text("CALL SP_KDS_Despachar(:id_origen, :origen, :id_usuario)"),
            {
                'id_origen': id_origen, 
                'origen': origen, 
                'id_usuario': current_user.id_usuario
            }
        )
        db.session.commit()
        
        # Guardamos en bitácora
        audit.log_action(
            module_name="logs_kds", 
            action=f"Ticket {origen} Despachado", 
            details={"id": id_origen, "tipo": origen},
            level="INFO"
        )
        
        flash(f'¡{origen} marcada como LISTA y materia prima descontada!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error en KDS al despachar: {e}")
        flash('Hubo un error al despachar la orden. Verifica que tengas suficiente stock de insumos.', 'error')
        
    return redirect(url_for('tablero_kds.principal'))