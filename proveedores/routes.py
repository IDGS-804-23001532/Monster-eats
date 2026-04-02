from flask import render_template, request, url_for, flash, redirect
from . import proveedor
from sqlalchemy.exc import OperationalError
from models import db
from models import CategoriaProveedor, Proveedor
from extensions import limiter
import forms
from sanitizador import Sanitizador
from flask_security import login_required
from flask_security.decorators import roles_required


@proveedor.route("/proveedores", methods=['GET', 'POST'])
@login_required
@roles_required('gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def proveedores():
    create_form = forms.ProveedorForm(request.form)

    # Tomamos la cadena de texto que se escribio en la busqueda
    busqueda = request.args.get('q', '').strip()

    sql_query = "SELECT * FROM vista_proveedores WHERE activo = 1"
    parametros = {}

    if busqueda:
        # Buscamos coincidencias entre el nombre_empresa y rfc
        sql_query += " AND (LOWER(nombre_empresa) LIKE LOWER(:busqueda) OR UPPER(rfc) LIKE UPPER(:busqueda))"
        parametros['busqueda'] = f"%{busqueda}%"

    # Ejecutamos el query
    proveedores = db.session.execute(
        db.text(sql_query),
        parametros
    ).mappings().all()

    # Cargamos la categoria disponibles
    lista_categorias = CategoriaProveedor.query.all()

    # Llenar la lista con la lista_categorias disponibles a seleccionar al SelectField
    create_form.categoria_proveedor.choices = [(c.id_categoria_proveedor, c.nombre) for c in lista_categorias]

    # Ahora vamos a poner una opcion por defecto al inicio
    create_form.categoria_proveedor.choices.insert(0, (0, 'Selecciona una categoria'))

    if request.method == 'POST' and create_form.validate():
        # Tomamos el id seleccionado de la categoria
        id_categoria_seleccionada = create_form.categoria_proveedor.data
        
        # Validamos para que no sea 0 por defecto
        if id_categoria_seleccionada == 0:
            flash('Por favor, selecciona una categoría', 'error')
            return redirect(url_for('proovedor.proveedores'))
            
        nombre_empresa = Sanitizador.limpiar_texto(create_form.nombre_empresa.data)
        nombre_contacto = Sanitizador.limpiar_texto(create_form.nombre_contacto.data)
        apellido_pa = Sanitizador.limpiar_texto(create_form.apellido_pa.data)
        apellido_ma = Sanitizador.limpiar_texto(create_form.apellido_ma.data)
        telefono = Sanitizador.limpiar_texto(create_form.telefono.data)
        email = Sanitizador.limpiar_email(create_form.email.data)
        rfc = Sanitizador.limpiar_texto(create_form.rfc.data)
        direccion = Sanitizador.limpiar_texto(create_form.direccion.data)
            
        try:
            # Llamamos el stored procedure
            db.session.execute(
                db.text('CALL sp_crear_proveedor(:nombre_empresa, :nombre_contacto, :apellido_pa, :apellido_ma, :telefono, :email, :rfc, :direccion, :id_categoria_proveedor)'),
                {
                    'nombre_empresa': nombre_empresa,
                    'nombre_contacto': nombre_contacto,
                    'apellido_pa': apellido_pa,
                    'apellido_ma': apellido_ma,
                    'telefono': telefono,
                    'email': email,
                    'rfc': rfc,
                    'direccion': direccion,
                    'id_categoria_proveedor': id_categoria_seleccionada
                }
            )
            
            db.session.commit()
            flash('Proveedor registrado con éxito', 'success')
            return redirect(url_for('proveedor.proveedores'))
            
        except OperationalError as e:
            db.session.rollback()

            # Atrapamos el error
            # mensaje_error = e.orig.args[1]
            flash('El nombre o RFC ya esta en uso', 'error')


    return render_template('proveedores/proveedor.html', form = create_form, proveedores = proveedores, categorias = lista_categorias)

@proveedor.route("/proveedores/actualizar/<int:id>", methods=['POST'])
@login_required
@roles_required('gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def actualizar_proveedor(id):
    create_form = forms.ProveedorForm(request.form)

    # Verificamos que el proveedor exista
    proveedor_existente = Proveedor.query.filter_by(id_proveedor = id).first()

    if not proveedor_existente:
        flash('El proveedor que intentas actualizar no existe', 'error')
        return redirect(url_for('proveedor.proveedores'))
    
    # Rellenamos las opciones del SelectField para validar
    lista_categorias = CategoriaProveedor.query.all()
    create_form.categoria_proveedor.choices = [(c.id_categoria_proveedor, c.nombre) for c in lista_categorias]
    create_form.categoria_proveedor.choices.insert(0, (0, 'Selecciona una categoria'))

    if not create_form.validate():
        flash('Datos invalidos o token caducado', 'error')
        return redirect(url_for('proveedor.proveedores'))

    # 3. Validamos que no hayan escogido la opción 0
    id_categoria_seleccionada = create_form.categoria_proveedor.data
    if id_categoria_seleccionada == 0:
        flash('Por favor, selecciona una categoría válida', 'error')
        return redirect(url_for('proveedores.proveedor'))
    

    nombre_empresa = Sanitizador.limpiar_texto(create_form.nombre_empresa.data)
    nombre_contacto = Sanitizador.limpiar_texto(create_form.nombre_contacto.data)
    apellido_pa = Sanitizador.limpiar_texto(create_form.apellido_pa.data)
    apellido_ma = Sanitizador.limpiar_texto(create_form.apellido_ma.data)
    telefono = Sanitizador.limpiar_texto(create_form.telefono.data)
    email = Sanitizador.limpiar_email(create_form.email.data)
    rfc = Sanitizador.limpiar_texto(create_form.rfc.data)
    direccion = Sanitizador.limpiar_texto(create_form.direccion.data)

    try:
        # 5. Llamamos al stored procedure
        db.session.execute(
            db.text('CALL sp_actualizar_proveedor(:id_proveedor, :nombre_empresa, :nombre_contacto, :apellido_pa, :apellido_ma, :telefono, :email, :rfc, :direccion, :id_categoria_proveedor)'),
            {
                'id_proveedor': id,
                'nombre_empresa': nombre_empresa,
                'nombre_contacto': nombre_contacto,
                'apellido_pa': apellido_pa,
                'apellido_ma': apellido_ma,
                'telefono': telefono,
                'email': email,
                'rfc': rfc,
                'direccion': direccion,
                'id_categoria_proveedor': id_categoria_seleccionada
            }
        )
    
        db.session.commit()
        flash('Proveedor actualizado con éxito', 'success')
        
    except OperationalError as e:
        db.session.rollback()
        # Atrapamos si intentan poner un RFC o Empresa que ya le pertenece a otro
        mensaje_error = e.orig.args[1]
        flash('El nombre o RFC ya esta en uso' , 'error')

    # Al final, SIEMPRE redirigimos a la ruta principal que es la que dibuja todo
    return redirect(url_for('proveedor.proveedores'))

@proveedor.route("/proveedores/eliminar/<int:id>", methods=['POST'])
@login_required
@roles_required('gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def eliminar_proveedor(id):
    create_form = forms.CategoriaProveedorForm(request.form)

    if request.method == 'POST' and create_form.validate():
        try:
            db.session.execute(
                db.text('CALL sp_eliminar_proveedor(:id)'),
                {'id': id}
            )

            db.session.commit()
            flash("Se elimino con exito", 'success')
        except:
            db.session.rollback()
            flash("Error al eliminar el proveedor", 'error')

    return redirect(url_for('proveedor.proveedores'))

@proveedor.route("/categorias", methods=['GET', 'POST'])
@login_required
@roles_required('gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def categorias():
    create_form = forms.CategoriaProveedorForm(request.form)

    categoria_proveedor = CategoriaProveedor.query.all()

    if request.method == 'POST':
        nombre_categoria = Sanitizador.limpiar_texto(create_form.nombre.data)

        if not nombre_categoria:
            create_form.validate()
            flash('El nombre de la categoria no puede estar vacia', 'error')
            return redirect(url_for('proveedor.categorias'))

        try:
            # Llamamos el stored procedure
            db.session.execute(
                db.text('CALL sp_crear_categoria_proveedor(:nombre)'),
                {'nombre': nombre_categoria}
            )

            db.session.commit()
            flash('Categoria creada con exito', 'success')
            return redirect(url_for('proveedor.categorias'))
        except OperationalError as e:
            db.session.rollback()

            # Si falla, mandamos el mensaje que ya existe
            flash(f'Esa categoria ya existe', 'error')
            return redirect(url_for('proveedor.categorias'))

    return render_template('proveedores/categorias.html', form = create_form, categoria_proveedor = categoria_proveedor)

@proveedor.route("/categorias/actualizar/<int:id>", methods=['GET', 'POST'])
@login_required
@roles_required('gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def actualizar_categoria(id):
    create_form = forms.CategoriaProveedorForm(request.form)

    if request.method == 'POST':
        nombre_categoria = Sanitizador.limpiar_texto(create_form.nombre.data)

        if not nombre_categoria:
            create_form.validate()
            flash('El nombre de la categoria no debe estar vacía', 'error')
            return redirect(url_for('proveedor.categorias'))
        
        try:
            # Llamamos el stored procedure
            db.session.execute(
                db.text('CALL sp_actualizar_categoria_proveedor(:id, :nombre)'),
                {'id': id, 'nombre': nombre_categoria}
            )

            db.session.commit()
            flash('Categoria actualizada con exito', 'success')
            return redirect(url_for('proveedor.categorias'))
        except OperationalError as e:
            db.session.rollback()

            # Mostrar mensaje de error
            flash('Esa categoria ya existe', 'error')
            return redirect(url_for('proveedor.categorias'))

    return render_template('proveedores/categorias.html', form = create_form)

@proveedor.route("/categorias/eliminar/<int:id>", methods=['POST'])
@login_required
@roles_required('gerente')
@limiter.limit('8 per minute') # 8 request por minuto
def eliminar_categoria(id):
    create_form = forms.CategoriaProveedorForm(request.form)

    if request.method == 'POST' and create_form.validate():
        try:
            db.session.execute(
                db.text('CALL sp_eliminar_categoria_proveedor(:id)'),
                {'id': id}
            )
            db.session.commit()
            flash('Categoría eliminada con éxito', 'success')
            
        except OperationalError as e:
            db.session.rollback()
            # Atrapa el error si la categoría está en uso por un proveedor
            flash('No puedes eliminar esta categoría porque ya tiene proveedores asignados.', 'error')

    return redirect(url_for('proveedor.categorias'))
