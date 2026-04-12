from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import Insumo, UnidadMedida, db
from forms import CreateInsumoForm, EditInsumoForm
from . import insumos
from flask_wtf.csrf import CSRFProtect
from audit_logger import audit
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted


@login_required
@roles_accepted('Gerente', 'gerente')
@insumos.route('/insumos')
def index():
    search_query = request.args.get('search_query', '')
    if search_query:
        # Busca coincidencias parciales sin importar mayúsculas o minúsculas
        insumos = Insumo.query.filter(Insumo.nombre.ilike(f'%{search_query}%')).all()
    else:
        insumos = Insumo.query.all()
    
    unidades_medida = UnidadMedida.query.all()
    create_form = CreateInsumoForm()
    edit_form = EditInsumoForm()
    choices = [(um.id_unidad_medida, um.nombre) for um in unidades_medida]
    create_form.id_unidad_medida.choices = choices
    edit_form.id_unidad_medida.choices = choices
    return render_template('insumos/index.html', insumos=insumos, search_query=search_query, unidades_medida=unidades_medida, create_form=create_form, edit_form=edit_form)

@insumos.route('/limpiar_busqueda')
def limpiar_busqueda():
    return redirect(url_for('insumos.index'))


@insumos.route("/nuevo_insumo", methods=['POST'])
def nuevo_insumo():
    create_form = CreateInsumoForm(request.form)
    unidades_medida = UnidadMedida.query.all()
    choices = [(um.id_unidad_medida, um.nombre) for um in unidades_medida]
    create_form.id_unidad_medida.choices = choices
    
    if create_form.validate():
        nombre_insertado = create_form.nombre.data.strip()
        
        # Validación para evitar que truene xd
        insumo_existente = Insumo.query.filter(Insumo.nombre.ilike(nombre_insertado)).first()
        
        if insumo_existente:
            # Manda el error por que ya existe perro jajaja por noob :v
            create_form.nombre.errors.append(f'El insumo "{nombre_insertado}" ya existe')
        else:
            # Procesar los datos del formulario de manera segura de la tabla de insumos recuerda no le muevas a esto
            insumo = Insumo(
                nombre=nombre_insertado,
                id_unidad_medida=create_form.id_unidad_medida.data,
                costo_unitario=create_form.costo_unitario.data,
                porcentaje_merma=create_form.porcentaje_merma.data,
                activo=True
            )
            db.session.add(insumo)
            db.session.commit()
            
            # --- REGISTRO DE AUDITORÍA MONGO ---
            audit.log_action("Insumos", "CREACIÓN", details={
                "id": insumo.id_insumo,
                "nombre": insumo.nombre,
                "costo": float(insumo.costo_unitario)
            })
            
            return redirect(url_for('insumos.index'))
    
    # Si falla la validación, es por que no insertaste algo perro jajaja por noob :v
    search_query = request.args.get('search_query', '')
    insumos_list = Insumo.query.all()
    edit_form = EditInsumoForm()
    edit_form.id_unidad_medida.choices = choices
    return render_template('insumos/index.html', 
                         insumos=insumos_list, 
                         search_query=search_query, 
                         unidades_medida=unidades_medida, 
                         create_form=create_form, 
                         edit_form=edit_form,
                         show_modal='nuevoInsumo')

@insumos.route("/editar_insumo", methods=['GET', 'POST'])
def editar_insumo():
    # Inicializamos el formulario con los datos del request (POST) o vacío (GET)
    edit_form = EditInsumoForm(request.form)
    unidades_medida = UnidadMedida.query.all()
    choices = [(um.id_unidad_medida, um.nombre) for um in unidades_medida]
    edit_form.id_unidad_medida.choices = choices

    if request.method == 'GET':
        # Buscamos el insumo por el ID
        id_insumo = request.args.get('id')
        insumo = Insumo.query.get(id_insumo)
        
        if not insumo:
            flash('Insumo no encontrado', 'error') 
            return redirect(url_for('insumos.index'))
        
        # Pre-llenamos el formulario con los datos de la base de datos
        edit_form.id_insumo.data = insumo.id_insumo
        edit_form.nombre.data = insumo.nombre
        edit_form.costo_unitario.data = insumo.costo_unitario
        edit_form.id_unidad_medida.data = insumo.id_unidad_medida
        edit_form.porcentaje_merma.data = insumo.porcentaje_merma
        edit_form.activo.data = 1 if insumo.activo else 0
        
        # Aqui hacemos para que el modal de edición se abra
        search_query = request.args.get('search_query', '')
        insumos_list = Insumo.query.all()
        create_form = CreateInsumoForm()
        create_form.id_unidad_medida.choices = choices
        return render_template('insumos/index.html', 
                             insumos=insumos_list, 
                             search_query=search_query, 
                             unidades_medida=unidades_medida, 
                             create_form=create_form, 
                             edit_form=edit_form,
                             show_modal='editInsumoModal')

    if request.method == 'POST':
        if edit_form.validate():
            insumo = Insumo.query.get(edit_form.id_insumo.data)
            if insumo:
                nombre_insertado = edit_form.nombre.data.strip()
                
                # Validación para que no truene la base de datos si ya existe el nombre
                insumo_existente = Insumo.query.filter(
                    Insumo.nombre.ilike(nombre_insertado),
                    Insumo.id_insumo != insumo.id_insumo
                ).first()
                
                if insumo_existente:
                    edit_form.nombre.errors.append(f'El insumo "{nombre_insertado}" ya existe')
                else:
                    insumo.nombre = nombre_insertado
                    insumo.id_unidad_medida = edit_form.id_unidad_medida.data
                    insumo.costo_unitario = edit_form.costo_unitario.data
                    insumo.porcentaje_merma = edit_form.porcentaje_merma.data
                    insumo.activo = bool(int(edit_form.activo.data))
                    db.session.commit()
                    
                    # --- REGISTRO DE AUDITORÍA MONGO ---
                    audit.log_action("Insumos", "EDICIÓN", details={
                        "id": insumo.id_insumo,
                        "nombre": insumo.nombre,
                        "activo": insumo.activo
                    })
                    
                    return redirect(url_for('insumos.index'))
    
    # Si falla la validación en POST, volvemos a mostrar el modal con errores
    search_query = request.args.get('search_query', '')
    insumos_list = Insumo.query.all()
    create_form = CreateInsumoForm()
    create_form.id_unidad_medida.choices = choices
    return render_template('insumos/index.html', 
                         insumos=insumos_list, 
                         search_query=search_query, 
                         unidades_medida=unidades_medida, 
                         create_form=create_form, 
                         edit_form=edit_form,
                         show_modal='editInsumoModal')

from sqlalchemy.exc import IntegrityError

@insumos.route('/eliminar_insumo', methods=['GET', 'POST'])
def eliminar():
    unidades_medida = UnidadMedida.query.all()
    choices = [(um.id_unidad_medida, um.nombre) for um in unidades_medida]
    
    if request.method == 'GET':
        id_insumo = request.args.get('id')
        insumo = Insumo.query.get(id_insumo)
        
        if not insumo:
            flash('Insumo no encontrado', 'error')
            return redirect(url_for('insumos.index'))
        
        # Renderizamos la página con el modal de eliminar abierto
        search_query = request.args.get('search_query', '')
        insumos_list = Insumo.query.all()
        create_form = CreateInsumoForm()
        create_form.id_unidad_medida.choices = choices
        edit_form = EditInsumoForm()
        edit_form.id_unidad_medida.choices = choices
        return render_template('insumos/index.html',
                             insumos=insumos_list,
                             search_query=search_query,
                             unidades_medida=unidades_medida,
                             create_form=create_form,
                             edit_form=edit_form,
                             delete_insumo=insumo,
                             show_modal='eliminarInsumoModal')
    
    if request.method == 'POST':
        id_insumo = request.form.get('id_insumo')
        insumo = Insumo.query.get(id_insumo)
        if not insumo:
            flash('Insumo no encontrado para eliminar', 'error')
            return redirect(url_for('insumos.index'))
        
        try:
            db.session.delete(insumo)
            db.session.commit()
            
            # --- REGISTRO DE AUDITORÍA MONGO ---
            audit.log_action("Insumos", "ELIMINACIÓN", details={
                "id": insumo.id_insumo,
                "nombre": insumo.nombre
            })
            
            flash('Insumo eliminado correctamente', 'success')
        except IntegrityError:
            db.session.rollback()
            audit.log_action("Insumos", "INTENTO FALLIDO ELIMINAR", details={
                "id_insumo": insumo.id_insumo,
                "nombre": insumo.nombre,
                "motivo": "Violación de integridad (historial existente asociado al insumo)",
                "usuario": current_user.email
            })
            flash('No se puede eliminar el insumo porque tiene historial asociado (ej. compras). Recomendación: desactívalo desde "Editar".', 'error')
        except Exception as e:
            db.session.rollback()
            audit.log_action("Insumos", "ERROR ELIMINAR", details={
                "id_insumo": insumo.id_insumo,
                "nombre": insumo.nombre,
                "error": str(e),
                "usuario": current_user.email
            })
            flash(f'Error al eliminar el insumo: {str(e)}', 'error')
            
        return redirect(url_for('insumos.index'))

