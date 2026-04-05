from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, Persona, Role
from werkzeug.security import generate_password_hash
import uuid
from . import usuarios_bp
import forms

@usuarios_bp.route('/')
def index():
    search = request.args.get('search')
    if search:
        # JOIN explícito para evitar problemas de lazy loading
        usuarios = db.session.query(User).join(Persona, User.id_persona == Persona.id_persona).filter(
            (Persona.nombre.like(f'%{search}%')) | 
            (Persona.apellido_pa.like(f'%{search}%')) |
            (Persona.apellido_ma.like(f'%{search}%'))
        ).all()
    else:
        usuarios = User.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios)


@usuarios_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    form = forms.UsuarioForm()
    form.rol_id.choices = [(r.id_rol, r.name) for r in Role.query.all()]

    if form.validate_on_submit():
        try:
            # 1. Crear la Persona
            nueva_persona = Persona(
                nombre=form.nombre.data,
                apellido_pa=form.apellido_pa.data,
                apellido_ma=form.apellido_ma.data if form.apellido_ma.data else '',  # NOT NULL en BD
                fecha_nac=form.fecha_nacimiento.data,
                telefono=form.telefono.data if form.telefono.data else None
            )
            db.session.add(nueva_persona)
            db.session.flush()  # Esto asigna id_persona

            # 2. Crear el User
            nuevo_usuario = User(
                id_persona=nueva_persona.id_persona,
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                intentos_fallidos=0  # Valor por defecto explícito
            )
            
            # 3. Asignar Rol
            rol = Role.query.get(form.rol_id.data)
            if rol:
                nuevo_usuario.roles.append(rol)

            db.session.add(nuevo_usuario)
            db.session.commit()
            
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('usuarios.index'))
            
        except Exception as e:
            db.session.rollback()
            print(f"ERROR al crear usuario: {str(e)}")
            flash(f'Error al registrar: {str(e)}', 'danger')
    
    return render_template('usuarios/crear.html', form=form)


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = User.query.get_or_404(id)
    
    # ✅ CORREGIDO: Usar el backref correctamente
    persona = usuario.datos_personales
    
    # Si por alguna razón no existe la persona (no debería pasar)
    if not persona:
        flash('Error: El usuario no tiene datos personales asociados', 'danger')
        return redirect(url_for('usuarios.index'))
    
    form = forms.UsuarioForm(obj=persona)
    form.rol_id.choices = [(r.id_rol, r.name) for r in Role.query.all()]
    
    if request.method == 'GET':
        form.email.data = usuario.email
        form.fecha_nacimiento.data = persona.fecha_nac
        form.telefono.data = persona.telefono
        if usuario.roles:
            form.rol_id.data = usuario.roles[0].id_rol

    if form.validate_on_submit():
        try:
            # 1. Actualizar Persona
            persona.nombre = form.nombre.data
            persona.apellido_pa = form.apellido_pa.data
            persona.apellido_ma = form.apellido_ma.data if form.apellido_ma.data else ''
            persona.fecha_nac = form.fecha_nacimiento.data
            persona.telefono = form.telefono.data if form.telefono.data else None
            
            # 2. Actualizar User
            usuario.email = form.email.data
            if form.password.data:
                usuario.password = generate_password_hash(form.password.data)
            # fs_uniquifier NO se modifica, se mantiene el original
            
            # 3. Actualizar Rol
            nuevo_rol = Role.query.get(form.rol_id.data)
            if nuevo_rol:
                usuario.roles = [nuevo_rol]

            db.session.commit()
            flash('Colaborador actualizado correctamente', 'success')
            return redirect(url_for('usuarios.index'))
            
        except Exception as e:
            db.session.rollback()
            print(f"ERROR al actualizar usuario: {str(e)}")
            flash(f'Error al actualizar: {str(e)}', 'danger')

    return render_template('usuarios/editar.html', form=form, usuario=usuario)


@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    usuario = User.query.get_or_404(id)
    try:
        usuario.active = not usuario.active
        db.session.commit()
        estado = "activado" if usuario.active else "desactivado"
        flash(f'Usuario {estado} con éxito', 'info')
    except Exception as e:
        db.session.rollback()
        print(f"ERROR al cambiar estado: {str(e)}")
        flash(f'Error al cambiar estado: {str(e)}', 'danger')
    
    return redirect(url_for('usuarios.index'))