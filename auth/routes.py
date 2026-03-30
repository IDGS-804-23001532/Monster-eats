from flask import render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import forms
from . import auth
from sanitizador import Sanitizador
from models import Usuario, Persona, db
from flask_security import login_required
from flask_security.utils import login_user, logout_user
from datetime import datetime, timedelta, date
import uuid

import logging

@auth.route("/login", methods=["GET", "POST"])
def login():
    create_form = forms.LoginForm(request.form)

    if request.method == "POST":
        create_form.validate()
        email = Sanitizador.limpiar_email(create_form.email.data)
        password = create_form.password.data.strip()
        remember = True if request.form.get('remember') else False

        # Consultamos si el usuario existe con ese email
        usuario = Usuario.query.filter_by(email = email).first()


        # Verificar si el usuario existe
        if usuario:
            # Revisamos si su cuenta esta bloqueada
            if usuario.bloqueado_hasta:
                if datetime.now() < usuario.bloqueado_hasta:
                    # Si sigue castigado, calculamos cuantos minutos le falta
                    tiempo_restante = usuario.bloqueado_hasta - datetime.now()
                    minutos = int(tiempo_restante.total_seconds() // 60)
                    flash(f'Tu cuenta ha sido bloqueada por {minutos} minutos, intente despues')
                    return redirect(url_for('auth.login'))
                else:
                    # En caso de que ya pase el tiempo, le quitamos el castigo
                    usuario.bloqueado_hasta = None
                    db.session.commit()

            # Verificamos si es correcto el password
            if not check_password_hash(usuario.password, password):
                # Incrementamos los intentos fallidos
                usuario.intentos_fallidos += 1

                if usuario.intentos_fallidos >= 5:
                    usuario.bloqueado_hasta = datetime.now() + timedelta(minutes = 30)
                    usuario.intentos_fallidos = 0
                    flash(f"Por seguridad, se bloqueo tu cuenta temporalmente, espera 30 minutos")
                else :
                    restantes = 5 - usuario.intentos_fallidos
                    flash(f'Contraseña incorrecta. Te quedan {restantes} intentos')

                db.session.commit()
                return redirect(url_for('auth.login'))
            
            # En caso de que haya sido correcto la contraseña
            # Reseteamos los intentos fallidos
            usuario.intentos_fallidos = 0
            db.session.commit()

            login_user(usuario, remember = remember)
            return redirect(url_for('index'))
        else:
            flash('El correo y/o contraseña son incorrectos')
            return redirect(url_for('auth.login'))

    return render_template("auth/login.html", form=create_form)

@auth.route("/crear_diego")
def crear_diego():
    # 1. CREAMOS LOS ROLES SI NO EXISTEN
    # Usamos user_datastore que es la herramienta oficial de Flask-Security
    from app import user_datastore # Importamos el datastore desde tu app.py

    rol_admin = user_datastore.find_or_create_role(name='gerente', descripcion='Gerente General')
    rol_caja = user_datastore.find_or_create_role(name='caja', descripcion='Personal de Caja')
    rol_cocina = user_datastore.find_or_create_role(name='cocina', descripcion='Personal de Cocina')
    db.session.commit()

    # 2. Verificamos si ya existes
    usuario_existente = Usuario.query.filter_by(email="diego@gmail.com").first()
    
    if usuario_existente:
        # Si ya existes pero no tienes el rol, te lo asignamos
        if not usuario_existente.has_role('gerente'):
            user_datastore.add_role_to_user(usuario_existente, rol_admin)
            db.session.commit()
            return "El usuario Diego ya existía, pero ahora es oficialmente Administrador. ¡Ve a loguearte!"
        return "El usuario Diego ya existe y ya es Administrador. ¡Ve a loguearte!"

    # 3. Si no existes, creamos tu Persona
    diego_persona = Persona(
        nombre="Diego Alejandro",
        apellido_pa="Gonzalez",
        apellido_ma="Gaytan",
        fecha_nac=date(2005, 9, 24)
    )
    db.session.add(diego_persona)
    db.session.flush()

    # 4. Creamos tu Usuario
    diego_usuario = user_datastore.create_user(
        id_persona=diego_persona.id_persona,
        email="diego@gmail.com",
        password=generate_password_hash("diego123#", method='pbkdf2:sha256'),
        active=True,
        fs_uniquifier=uuid.uuid4().hex,
        intentos_fallidos=0
    )
    
    # 5. ¡TE ASIGNAMOS EL ROL!
    user_datastore.add_role_to_user(diego_usuario, rol_admin)
    db.session.commit()

    return "¡Usuario Diego creado exitosamente como Administrador! Ya puedes ir a /login"

@auth.route("/crear_cajero")
def crear_cajero():
    from app import user_datastore 

    # 1. Aseguramos que el rol de caja exista
    rol_caja = user_datastore.find_or_create_role(name='caja', descripcion='Personal de Caja')
    db.session.commit()

    # 2. Verificamos si Cristo ya existe
    usuario_existente = Usuario.query.filter_by(email="cristo@gmail.com").first()
    
    if usuario_existente:
        if not usuario_existente.has_role('caja'):
            user_datastore.add_role_to_user(usuario_existente, rol_caja)
            db.session.commit()
            return "El usuario Cristo ya existía, pero ahora es oficialmente Cajero."
        return "El usuario Cristo ya existe y ya tiene el rol de Caja."

    # 3. Creamos el registro en Persona
    cristo_persona = Persona(
        nombre="Cristo",
        apellido_pa="Cajero",
        apellido_ma="Monster",
        fecha_nac=date(2002, 5, 15)
    )
    db.session.add(cristo_persona)
    db.session.flush()

    # 4. Creamos el Usuario con su hash seguro
    cristo_usuario = user_datastore.create_user(
        id_persona=cristo_persona.id_persona,
        email="cristo@gmail.com",
        password=generate_password_hash("cristo123#", method='pbkdf2:sha256'),
        active=True,
        fs_uniquifier=uuid.uuid4().hex,
        intentos_fallidos=0
    )
    
    # 5. ¡Le asignamos el rol restrictivo!
    user_datastore.add_role_to_user(cristo_usuario, rol_caja)
    db.session.commit()

    return "¡Cajero Cristo creado exitosamente! Ingresa con cristo@monstereats.com y contraseña caja123#"

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))