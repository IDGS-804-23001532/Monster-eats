from flask import render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import limiter
import forms
from . import auth
from sanitizador import Sanitizador
from models import Usuario, Persona, db
from flask_security import login_required
from flask_security.utils import login_user, logout_user
from datetime import datetime, timedelta
import uuid

import logging

@auth.route("/login", methods=["GET", "POST"])
def login():
    try:
        create_form = forms.LoginForm(request.form)

        if request.method == "POST" and create_form.validate():
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
                        logging.warning(f'Intento de inicio de sesion bloqueada del {email}')
                        flash(f'Tu cuenta ha sido bloqueada por {minutos} minutos, intente despues', 'error')
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
                        logging.warning(f'Se bloqueo la cuenta temporalmente a {email} por 30 minutos')
                        flash(f"Por seguridad, se bloqueo tu cuenta temporalmente, espera 30 minutos", 'error')
                    else :
                        restantes = 5 - usuario.intentos_fallidos
                        logging.warning(f'Intento de inicio sesión fallido por {email}, intentos: {restantes}')
                        flash(f'Contraseña incorrecta. Te quedan {restantes} intentos', 'error')

                    db.session.commit()
                    return redirect(url_for('auth.login'))
                
                # En caso de que haya sido correcto la contraseña
                # Reseteamos los intentos fallidos
                usuario.intentos_fallidos = 0
                db.session.commit()
                logging.info(f'Inicio de sesion exisoto de {email}')
                login_user(usuario, remember = remember)
                return redirect(url_for('dashboard.index'))
            else:
                logging.warning(f'Intento de inicio de sesión sin datos sin coincidir {email}')
                flash('El correo y/o contraseña son incorrectos', 'error')
                return redirect(url_for('auth.login'))
    except Exception as error:
        logging.warning(f'Error al inicio de sesion del usuario {email}: {str(error)}')
    return render_template("auth/login.html", form=create_form)

@auth.route("/register", methods=['GET', 'POST'])
@limiter.limit("3 per minute") # 3 peticiones por minuto por ip
def register():
    try:
        from app import user_datastore
        create_form = forms.RegisterForm(request.form)

        if request.method == "POST" and create_form.validate():

            # Formulario
            nombre = Sanitizador.limpiar_texto(create_form.nombre.data)
            apellido_pa = Sanitizador.limpiar_texto(create_form.apellido_pa.data)
            apellido_ma = Sanitizador.limpiar_texto(create_form.apellido_ma.data)
            fecha_nac = create_form.fecha_nac.data
            telefono = Sanitizador.limpiar_texto(create_form.telefono.data)
            email = Sanitizador.limpiar_email(create_form.email.data)
            password = Sanitizador.limpiar_texto(create_form.password.data)

            # Consultamos si existe el usuario con el mismo correo
            usuario = Usuario.query.filter_by(email = email).first()

            # Comprobamos que exista el rol cliente
            rol_cliente = user_datastore.find_or_create_role(name = 'cliente', descripcion = 'Cliente en linea')
            db.session.commit()


            # Comprobamos si existe el correo, en caso de que si confudimos al atacante
            if usuario:
                logging.warning('f"Intento de registro con correo existente{email}')
                flash('Si tus datos son correctos, tu cuenta ha sido creada', 'success')
                return redirect(url_for('auth.login'))
            
            # Crear a persona
            nueva_persona = Persona(
                nombre = nombre,
                apellido_pa = apellido_pa,
                apellido_ma = apellido_ma,
                fecha_nac = fecha_nac,
                telefono = telefono
            )

            db.session.add(nueva_persona)
            db.session.flush() # Asigna el id, pero espera

            nuevo_usuario = user_datastore.create_user(
                id_persona = nueva_persona.id_persona,
                email = email,
                password = generate_password_hash(password, method = 'pbkdf2:sha256'),
                active = True,
                fs_uniquifier = uuid.uuid4().hex,
                intentos_fallidos = 0
            )

            # Asignamos el rol de cliente
            user_datastore.add_role_to_user(nuevo_usuario, rol_cliente)
            db.session.commit()

            logging.info(f'Nuevo cliente registrado{email}')

            # Mensaje real de exito :3
            flash('Cuenta creada exitosamente', 'success')
            return redirect(url_for('auth.login'))
    except Exception as error:
        db.session.rollback()
        logging.warning(f'Error critico en registro de un usuario: {str(error)}')
    return render_template('auth/register.html', form = create_form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))