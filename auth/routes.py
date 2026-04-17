from flask import render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import limiter
import forms
from . import auth
from audit_logger import audit
from sanitizador import Sanitizador
from models import Usuario, Persona, db
from flask_security import login_required, current_user
from flask_security.utils import login_user, logout_user
from datetime import datetime, timedelta
import uuid, random

import logging

@auth.route("/login", methods=["GET", "POST"])
def login():
    try:
        create_form = forms.LoginForm(request.form)

        if request.method == "POST" and create_form.validate():
            captcha_esperado = session.get('captcha_answer')
            captcha_usuario = create_form.captcha.data

            # Limpiamos la sesion para que no puedan reutilizarlo
            session.pop('captcha_answer', None)

            if captcha_esperado is None or captcha_usuario != captcha_esperado:
                flash('Respuesta captcha incorrecta. Intentalo de nuevo')
                return redirect(url_for('auth.login'))


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

                        audit.log_action(
                            module_name="logs_auth",
                            action="Intento de inicio de sesión en cuenta bloqueada",
                            details={
                                "email_intentando": email, "minutos_restantes": minutos
                            },
                            level="WARNING"
                        )

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

                        audit.log_action(
                            module_name="logs_auth",
                            action="Cuenta bloqueada temporalmente por intentos fallidos",
                            details={
                                "email_afectado": email, "limite_intentos": 5, "minutos_bloqueo": 30
                            },
                            level="WARNING"
                        )

                        flash(f"Por seguridad, se bloqueo tu cuenta temporalmente, espera 30 minutos", 'error')
                    else :
                        restantes = 5 - usuario.intentos_fallidos

                        audit.log_action(
                            module_name="logs_auth",
                            action="Intento fallido de inicio de sesión",
                            details={
                                "email_intentando": email, "intentos_restantes": restantes
                            },
                            level="WARNING"
                        )

                        logging.warning(f'Intento de inicio sesión fallido por {email}, intentos: {restantes}')
                        flash(f'Contraseña incorrecta. Te quedan {restantes} intentos', 'error')

                    db.session.commit()
                    return redirect(url_for('auth.login'))
                
                # En caso de que haya sido correcto la contraseña
                # Reseteamos los intentos fallidos
                usuario.intentos_fallidos = 0
                db.session.commit()

                # Generamos un codigo de 2FA
                codigo_2fa = str(random.randint(100000, 999999))

                # Guardamos datos temporalmente
                session['2fa_code'] = codigo_2fa
                session['2fa_user_email'] = usuario.email
                session['remember_me'] = remember

                # Enviamos el correo
                from flask_mail import Message
                from extensions import mail

                try:
                    msg = Message('Tu código de acceso - Monster Eats', 
                                  sender= 'no-reply@monstereats.com',
                                  recipients=[usuario.email])
                    
                    msg.body = f'Hola {usuario.persona.nombre}, \n\nTu código de verificación para entrar es: {codigo_2fa}\n\nSi no intentaste iniciar sesión, ignora este mensaje.'
                    mail.send(msg)
                    logging.info(f'Código 2FA enviado a {email}')
                except Exception as e:
                    logging.error(f'Error enviando correo 2FA a {email}: {e}')
                    flash('Ocurrio un error al enviar el código a tu correo, por favor intentelo después')
                    return redirect(url_for('auth.login'))
                
                return redirect(url_for('auth.verify_2fa'))
            else:
                logging.warning(f'Intento de inicio de sesión sin datos sin coincidir {email}')

                audit.log_action(
                    module_name="logs_auth",
                    action="Intento de inicio de sesión de usuario inexistente",
                    details={"email_intentado": email},
                    level="WARNING"
                )

                flash('El correo y/o contraseña son incorrectos', 'error')
                return redirect(url_for('auth.login'))
            
        # Generacion del captcha 
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operacion = random.choice(['+', '*'])

        # Guardamos el resultado
        session['captcha_answer'] = (num1 + num2) if operacion == '+' else (num1 * num2)

        # Creamos el texto de la pregunta para mandarlo a la vista
        captcha_question = f'¿Cuanto es {num1} {operacion} {num2}?'

        return render_template('auth/login.html', form = create_form, captcha_question = captcha_question)
    except Exception as error:
        logging.warning(f'Error al inicio de sesion del usuario {email}: {str(error)}')
        audit.log_action(module_name="logs_auth", action="Error crítico en login", details={"error": str(error)}, level="ERROR")
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

                audit.log_action(
                    module_name="logs_auth",
                    action="Intento de registro con correo existente",
                    details={"email_intentado": email},
                    level="WARNING"
                )

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

            audit.log_action(
                module_name="logs_auth",
                action="Registro de usuario exitoso",
                details={"email_nuevo_usuario": email, "id_persona": nueva_persona.id_persona},
                level="INFO"
            )

            # Mensaje real de exito :3
            flash('Cuenta creada exitosamente', 'success')
            return redirect(url_for('auth.login'))
    except Exception as error:
        db.session.rollback()
        logging.warning(f'Error critico en registro de un usuario: {str(error)}')
    return render_template('auth/register.html', form = create_form)

@auth.route("/crear-cajero-demo")
def crear_cajero_demo():
    from app import user_datastore

    try:
        email = "alexgonzalezgaytan@gmail.com"
        password_plana = "Diego123#"

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("El usuario cajero ya existe.", "info")
            return redirect(url_for("index"))

        rol_cajero = user_datastore.find_or_create_role(
            name="Cajero",
            descripcion="Registro de ventas en mostrador"
        )
        db.session.commit()

        telefono_demo = "4771200987"
        nueva_persona = Persona.query.filter_by(telefono=telefono_demo).first()
        if not nueva_persona:
            nueva_persona = Persona(
                nombre="Diego Alejandro",
                apellido_pa="Gonzalez",
                apellido_ma="Gaytan",
                telefono=telefono_demo
            )
            db.session.add(nueva_persona)
            db.session.flush()

        nuevo_usuario = user_datastore.create_user(
            id_persona=nueva_persona.id_persona,
            email=email,
            password=generate_password_hash(password_plana),
            active=True,
            fs_uniquifier=uuid.uuid4().hex,
            intentos_fallidos=0,
            bloqueado_hasta=None
        )

        user_datastore.add_role_to_user(nuevo_usuario, rol_cajero)
        db.session.commit()

        flash("Usuario cajero creado correctamente.", "success")
        return redirect(url_for("index"))

    except Exception as error:
        db.session.rollback()
        flash(f"No se pudo crear el usuario cajero: {str(error)}", "error")
        audit.log_action(module_name="logs_auth", action="Error crítico en registro", details={"error": str(error)}, level="ERROR")
        return redirect(url_for("index"))

@auth.route("/gerente-full")
def gerente_full():
    try:
        import uuid
        from werkzeug.security import generate_password_hash
        from models import Usuario, Persona, Rol, db
        from app import user_datastore

        email = "riveravalderramachristopherisa@gmail.com"
        password_plana = "Lagatita25"

        # 1. Buscamos o creamos el usuario
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            telefono_demo = "4771800650"
            nueva_persona = Persona.query.filter_by(telefono=telefono_demo).first()
            if not nueva_persona:
                nueva_persona = Persona(
                    nombre="Isaac",
                    apellido_pa="Rivera",
                    apellido_ma="Martinez",
                    telefono=telefono_demo
                )
                db.session.add(nueva_persona)
                db.session.flush()

            usuario = user_datastore.create_user(
                id_persona=nueva_persona.id_persona,
                email=email,
                password=generate_password_hash(password_plana),
                active=True,
                fs_uniquifier=uuid.uuid4().hex,
                intentos_fallidos=0,
                bloqueado_hasta=None
            )
        else:
            usuario.active = True
            usuario.password = generate_password_hash(password_plana)
            # Actualizamos el nombre para que sepa que es el nuevo
            usuario.persona.nombre = "Isaac"
            usuario.persona.apellido_pa = "Rivera"
            usuario.persona.apellido_ma = "Martinez"

        # 2. Lista de roles EXACTOS según layout.html
        # Nota: 'Cajero' es con C mayúscula en layout.html
        roles_a_asignar = [
            ("gerente", "Acceso total")
        ]

        # Limpiamos roles actuales para evitar duplicados o conflictos
        usuario.roles = []
        
        for nombre, desc in roles_a_asignar:
            rol = user_datastore.find_or_create_role(name=nombre, descripcion=desc)
            user_datastore.add_role_to_user(usuario, rol)
        
        db.session.commit()

        flash(f"¡ÉXITO! Usuario '{email}' configurado con rol Gerente. CIERRA SESIÓN Y ENTRA DE NUEVO.", "success")
        return redirect(url_for("auth.login"))

    except Exception as error:
        db.session.rollback()
        flash(f"Error crítico: {str(error)}", "error")
        return redirect(url_for("auth.login"))

@auth.route("/crear-cocinero-demo")
def crear_cocinero_demo():
    from app import user_datastore
    from models import Rol

    try:
        email = "demo@monstereats.com"
        password_plana = "Cocina123*"

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("El usuario de cocina ya existe.", "info")
            return redirect(url_for("auth.login"))

        # Intentamos obtener el rol por ID 4 (como indicó el usuario) o por nombre 'Cocina'
        rol_cocina = Rol.query.get(4)
        if not rol_cocina:
            rol_cocina = user_datastore.find_or_create_role(
                name="Cocina",
                descripcion="Personal de preparación de alimentos"
            )
        
        db.session.commit()

        telefono_demo = "2220009999"
        nueva_persona = Persona.query.filter_by(telefono=telefono_demo).first()
        if not nueva_persona:
            nueva_persona = Persona(
                nombre="Mariana",
                apellido_pa="Lopez",
                apellido_ma="Diaz",
                telefono=telefono_demo
            )
            db.session.add(nueva_persona)
            db.session.flush()

        nuevo_usuario = user_datastore.create_user(
            id_persona=nueva_persona.id_persona,
            email=email,
            password=generate_password_hash(password_plana),
            active=True,
            fs_uniquifier=uuid.uuid4().hex,
            intentos_fallidos=0,
            bloqueado_hasta=None
        )

        user_datastore.add_role_to_user(nuevo_usuario, rol_cocina)
        db.session.commit()
        
        flash(f"Usuario de cocina (Rol ID 4) creado: {email} / {password_plana}", "success")
        return redirect(url_for("auth.login"))

    except Exception as error:
        db.session.rollback()
        flash(f"No se pudo crear el usuario de cocina: {str(error)}", "error")
        return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    email_salida = current_user.email if current_user.is_authenticated else "Desconocido"
    logout_user()

    audit.log_action(
        module_name="logs_auth",
        action="Cierre de sesión",
        details={"email": email_salida},
        level="INFO"
    )

    return redirect(url_for('auth.login'))

@auth.route("/verify-2fa", methods=["GET", "POST"])
def verify_2fa():
    # Si intentan entrar a esta ruta sin haber pasado por el login, los regresamos
    if '2fa_user_email' not in session:
        return redirect(url_for('auth.login'))

    email_usuario = session.get('2fa_user_email')

    if request.method == "POST":
        codigo_ingresado = request.form.get("codigo")
        codigo_esperado = session.get("2fa_code")

        if codigo_ingresado and codigo_ingresado.strip() == codigo_esperado:
            # ¡Código correcto! Ahora sí iniciamos la sesión oficial
            usuario = Usuario.query.filter_by(email=email_usuario).first()
            if usuario:
                remember = session.get('remember_me', False)
                login_user(usuario, remember=remember)

                audit.log_action(
                    module_name="logs_auth",
                    action="Inicio de sesión exitoso (2FA)",
                    details={"email": email_usuario},
                    level="INFO"
                )

                # Limpiamos la basura temporal de la sesión
                session.pop('2fa_code', None)
                session.pop('2fa_user_email', None)
                session.pop('remember_me', None)

                # Priorizamos mandar al ERP si tienen cualquier rol de empleado
                if (current_user.has_role('gerente') or current_user.has_role('Gerente') or
                    current_user.has_role('Cajero') or current_user.has_role('cajero') or
                    current_user.has_role('Cocina') or current_user.has_role('cocina')):
                    return redirect(url_for('index'))
                elif current_user.has_role('cliente') or current_user.has_role('Cliente'):
                    return redirect(url_for('inicio'))
                else:
                    return redirect(url_for('index'))
        else:
            # El código no es válido
            audit.log_action(
                module_name="logs_auth",
                action="Fallo de verificación 2FA",
                details={"email": email_usuario},
                level="WARNING"
            )
            flash("El código no es válido o ha expirado. Vuelve a intentarlo.", "error")
            return redirect(url_for('auth.verify_2fa'))

    return render_template("auth/verify_2fa.html", email=email_usuario)

@auth.route("/restablecer-password", methods=['GET', 'POST'])
def restablecer_password():
    try:
        reset_form = forms.RestablecerPassForm(request.form)

        if request.method == 'POST' and reset_form.validate():
            email = Sanitizador.limpiar_email(reset_form.email.data)
            nueva_password = reset_form.nueva_password.data.strip()

            usuario = Usuario.query.filter_by(email=email).first()
            
            # Verificamos si existe el correo
            if not usuario:
                logging.warning(f'Intento de recuperación con correo no registrado: {email}')
                flash('Ese correo no está registrado. ¡Únete a la familia Monster Eats!', 'error')
                return redirect(url_for('auth.restablecer_password'))

            # Si existe, generamos código
            codigo_2fa = str(random.randint(100000, 999999))
            
            # Guardamos datos temporalmente en sesión, incluyendo la clave ya encriptada
            session['reset_2fa_code'] = codigo_2fa
            session['reset_email'] = email
            session['reset_new_password_hash'] = generate_password_hash(nueva_password, method='pbkdf2:sha256')

            # Enviamos el correo
            from flask_mail import Message
            from extensions import mail
            try:
                msg = Message('Restablecer contraseña - Monster Eats',
                              sender='no-reply@monstereats.com',
                              recipients=[usuario.email])
                msg.body = f'Hola {usuario.persona.nombre},\n\nTu código para restablecer tu contraseña es: {codigo_2fa}\n\nSi no solicitaste este cambio, ignora este mensaje.'
                mail.send(msg)
                logging.info(f'Código de recuperación enviado a {email}')
            except Exception as e:
                logging.error(f'Error enviando correo de recuperación a {email}: {e}')
                flash('Ocurrió un error al enviar el código. Inténtalo de nuevo.', 'error')
                return redirect(url_for('auth.restablecer_password'))

            return redirect(url_for('auth.verify_reset_2fa'))

        return render_template('auth/restablecer_contrasenia.html', form=reset_form)
    except Exception as error:
        logging.error(f'Error en restablecer_password: {str(error)}')
        flash('Ocurrió un error inesperado.', 'error')
        return redirect(url_for('auth.login'))


@auth.route("/verify-reset-2fa", methods=["GET", "POST"])
def verify_reset_2fa():
    # Evitar accesos directos
    if 'reset_email' not in session:
        return redirect(url_for('auth.login'))

    email_usuario = session.get('reset_email')

    if request.method == "POST":
        codigo_ingresado = request.form.get("codigo")
        codigo_esperado = session.get("reset_2fa_code")

        if codigo_ingresado and codigo_ingresado.strip() == codigo_esperado:
            # Código correcto: Actualizamos la contraseña
            usuario = Usuario.query.filter_by(email=email_usuario).first()
            if usuario:
                usuario.password = session.get('reset_new_password_hash')
                db.session.commit()

                audit.log_action(
                    module_name="logs_auth",
                    action="Contraseña restablecida exitosamente",
                    details={"email": email_usuario},
                    level="INFO"
                )

                # Limpiamos sesión
                session.pop('reset_2fa_code', None)
                session.pop('reset_email', None)
                session.pop('reset_new_password_hash', None)

                flash("¡Tu contraseña ha sido actualizada con éxito! Ya puedes iniciar sesión.", "success")
                return redirect(url_for('auth.login'))
        else:
            audit.log_action(
                module_name="logs_auth",
                action="Fallo 2FA en recuperación de contraseña",
                details={"email": email_usuario},
                level="WARNING"
            )
            flash("El código no es válido. Vuelve a intentarlo.", "error")
            return redirect(url_for('auth.verify_reset_2fa'))

    return render_template("auth/verify_reset_2fa.html", email=email_usuario)