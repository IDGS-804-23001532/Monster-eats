from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from sqlalchemy import text
from flask_security import login_required, roles_accepted, current_user
from audit_logger import audit
import traceback

tablero_kds = Blueprint('tablero_kds', __name__, url_prefix='/kds')

@tablero_kds.route('/')
@login_required
@roles_accepted('cocina', 'cocinero', 'gerente', 'administrador') 
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
@roles_accepted('cocina', 'cocinero', 'gerente', 'administrador')
def marcar_listo():
<<<<<<< Updated upstream
    # Recibimos el ID y si es de 'Venta' o 'Producción'
    id_origen = request.form.get('id_origen')
    origen = request.form.get('origen')

=======
    print("\n" + "="*60)
    print("🍳 KDS: INICIANDO PROCESO DE DESPACHO")
    print("="*60)

    # Recibimos los datos del frontend
    id_origen = request.form.get('id_origen')
    origen = request.form.get('origen')

    print(f" 1. Recibiendo petición del navegador:")
    print(f"   - Tipo: {origen} | ID: {id_origen} | Usuario: {current_user.email}")

>>>>>>> Stashed changes
    try:
        print("\n  2. Mandando la orden a MySQL (Ejecutando el SP)...")
        db.session.execute(
            text("CALL SP_KDS_Despachar(:id_origen, :origen, :id_usuario)"),
            {
                'id_origen': id_origen, 
                'origen': origen, 
                'id_usuario': current_user.id_usuario
            }
        )

        db.session.commit()
        print("\n 3. COMMIT EXITOSO: El inventario se ha actualizado permanentemente.")
        
        # Guardamos en bitácora local de NoSQL
        audit.log_action(
            module_name="logs_kds", 
            action=f"Ticket {origen} Despachado", 
            details={"id": id_origen, "tipo": origen},
            level="INFO"
        )
        
        flash(f'¡{origen} marcada como LISTA y materia prima descontada!', 'success')
        print(" Proceso terminado. Recargando página...\n")
        
    except Exception as e:
        db.session.rollback()
        print("\n" + "!"*50)
        print(" ERROR CRÍTICO AL DESPACHAR")
        print("!"*50)
        
        # Si MySQL falla (ej. por falta de inventario o validaciones), imprimimos su error nativo
        error_msg = str(e)
        print(f" Motivo del rechazo desde BD: {error_msg}")
        print("="*60 + "\n")
        
        flash('Hubo un error al despachar la orden. Verifica que el inventario sea suficiente.', 'error')
        
    return redirect(url_for('tablero_kds.principal'))