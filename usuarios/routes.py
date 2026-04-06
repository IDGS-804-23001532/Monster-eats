from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Usuario, Persona, Rol
from werkzeug.security import generate_password_hash
from sqlalchemy import text 
import uuid
import logging
from . import usuarios_bp
import forms

# Configurar logger para trazabilidad
logger = logging.getLogger(__name__)

@usuarios_bp.route('/')
def index():
    search = request.args.get('search')
    try:
        if search:
            # Usando text() para la consulta SQL
            query = text("""
                SELECT * FROM V_Usuarios_Detalle 
                WHERE nombre LIKE :search 
                OR apellido_pa LIKE :search 
                OR apellido_ma LIKE :search
            """)
            usuarios = db.session.execute(query, {'search': f'%{search}%'}).fetchall()
        else:
            # Usando text() para la consulta SQL
            query = text("SELECT * FROM V_Usuarios_Detalle")
            usuarios = db.session.execute(query).fetchall()
        
        return render_template('usuarios/index.html', usuarios=usuarios)
    
    except Exception as e:
        logger.error(f"Error en index de usuarios: {str(e)}")
        flash('Error al cargar la lista de usuarios', 'danger')
        return render_template('usuarios/index.html', usuarios=[])


@usuarios_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    form = forms.UsuarioForm()
    form.rol_id.choices = [(r.id_rol, r.name) for r in Rol.query.all()]

    if form.validate_on_submit():
        try:
            # Generar hash de la contraseña
            password_hash = generate_password_hash(form.password.data)
            fs_uniquifier = str(uuid.uuid4())
            
            # Ejecutar SP_Crear_Usuario con text()
            query = text("""
                CALL SP_Crear_Usuario(
                    :nombre, :apellido_pa, :apellido_ma, :fecha_nac, 
                    :telefono, :email, :password, :fs_uniquifier, :id_rol
                )
            """)
            db.session.execute(query, {
                'nombre': form.nombre.data,
                'apellido_pa': form.apellido_pa.data,
                'apellido_ma': form.apellido_ma.data if form.apellido_ma.data else '',
                'fecha_nac': form.fecha_nacimiento.data,
                'telefono': form.telefono.data,
                'email': form.email.data,
                'password': password_hash,
                'fs_uniquifier': fs_uniquifier,
                'id_rol': form.rol_id.data
            })
            db.session.commit()
            
            logger.info(f"Usuario creado exitosamente: {form.email.data}")
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('usuarios.index'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear usuario: {str(e)}")
            flash(f'Error al registrar: {str(e)}', 'danger')
    
    return render_template('usuarios/crear.html', form=form)


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    persona = usuario.persona
    
    form = forms.UsuarioForm(obj=persona)
    form.rol_id.choices = [(r.id_rol, r.name) for r in Rol.query.all()]
    
    if request.method == 'GET':
        form.email.data = usuario.email
        form.fecha_nacimiento.data = persona.fecha_nac
        form.telefono.data = persona.telefono
        if usuario.roles:
            form.rol_id.data = usuario.roles[0].id_rol
        # Hacer opcional la contraseña en edición
        form.password.validators = []

    if form.validate_on_submit():
        try:
            # Preparar contraseña (solo si se proporcionó una nueva)
            password_hash = None
            if form.password.data:
                password_hash = generate_password_hash(form.password.data)
            
            # Ejecutar SP_Editar_Usuario con text()
            query = text("""
                CALL SP_Editar_Usuario(
                    :id_usuario, :nombre, :apellido_pa, :apellido_ma, 
                    :fecha_nac, :telefono, :email, :password, :id_rol
                )
            """)
            db.session.execute(query, {
                'id_usuario': id,
                'nombre': form.nombre.data,
                'apellido_pa': form.apellido_pa.data,
                'apellido_ma': form.apellido_ma.data if form.apellido_ma.data else '',
                'fecha_nac': form.fecha_nacimiento.data,
                'telefono': form.telefono.data,
                'email': form.email.data,
                'password': password_hash,
                'id_rol': form.rol_id.data
            })
            db.session.commit()
            
            logger.info(f"Usuario actualizado: {form.email.data}")
            flash('Colaborador actualizado correctamente', 'success')
            return redirect(url_for('usuarios.index'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar usuario: {str(e)}")
            flash(f'Error al actualizar: {str(e)}', 'danger')

    return render_template('usuarios/editar.html', form=form, usuario=usuario)


@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        # Usar SP_Toggle_Estado_Usuario con text()
        query = text("CALL SP_Toggle_Estado_Usuario(:id_usuario)")
        db.session.execute(query, {'id_usuario': id})
        db.session.commit()
        
        # Obtener el estado actual para el mensaje
        usuario = Usuario.query.get_or_404(id)
        estado = "activado" if usuario.active else "desactivado"
        logger.info(f"Usuario {id} {estado}")
        flash(f'Usuario {estado} con éxito', 'info')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al cambiar estado del usuario {id}: {str(e)}")
        flash(f'Error al cambiar estado: {str(e)}', 'danger')
    
    return redirect(url_for('usuarios.index'))