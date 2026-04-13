from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, SelectField, DecimalField, HiddenField, EmailField, PasswordField, StringField, DateField, TelField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange, Length, Email, Regexp, Optional, ValidationError


class LoginForm(Form):
    email = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Formato de correo no válido')
    ])

    password = PasswordField('Password', [
        validators.DataRequired(message='El password es requerido'),
        validators.Length(min=8, message='El password debe tener al menos 8 carácteres')
    ])

    captcha = IntegerField('Captcha: ', [
        validators.DataRequired(message='El captcha es requerido')
    ])

class RegisterForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])

    apellido_pa = StringField('Apellido Paterno', [
        validators.DataRequired(message='El apellido paterno es requerido')
    ])

    apellido_ma = StringField('Apellido Materno', [
        validators.DataRequired(message='El apellido materno es requerido')
    ])

    fecha_nac = DateField('Fecha de Nacimiento', [
        validators.DataRequired(message='La fecha de nacimiento es requerido')
    ])

    telefono = TelField('Telefono', [
        validators.DataRequired(message='El telefono es requerido'),
        validators.Length(min = 10, message='Minimo son 10 digitos númericos'),
        validators.Regexp(r'^\d{10}$', message="El número debe tener exactamente 10 dígitos.")
    ])

    email = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Formato de correo no válido')
    ])

    password = PasswordField('Password', [
        validators.DataRequired(message='El password es requerido'),
        validators.Length(min=8, message='El password debe tener al menos 8 carácteres'),
        validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.')
    ])


class AjusteStockForm(FlaskForm):
    id_producto = HiddenField('ID Producto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad (sumar/restar)', validators=[
        DataRequired(message="Ingresa un número válido")
    ])
    motivo = TextAreaField('Motivo del ajuste', validators=[
        DataRequired(message="El motivo es obligatorio para la auditoría")
    ])
    submit = SubmitField('Guardar Ajuste')

# ==========================================================================
# FORMULARIOS DE PROVEEDORES E INSUMOS
# ==========================================================================

class CategoriaProveedorForm(Form):
    nombre = StringField('Nombre de la categoria', [
        validators.DataRequired(message='El nombre de la categoria es requerida')
    ])

class ProveedorForm(Form):
    nombre_empresa = StringField('Nombre de empresa', [
        validators.DataRequired(message = 'El nombre de empresa es requerida')
    ])
    nombre_contacto = StringField('Nombre del contacto', [
        validators.DataRequired(message='El nombre del contacto es requerido')
    ])
    apellido_pa = StringField('Apellido Paterno', [
        validators.DataRequired(message='El apellido paterno es requerido')
    ])
    apellido_ma = StringField('Apellido Materno', [
        validators.DataRequired(message='El apellido materno es requerido')
    ])
    telefono = TelField('Teléfono', [
        validators.DataRequired(message= 'El Teléfono es requerido'),
        validators.Length(min=10, message='El número debe tener 10 digitos'),
        validators.Regexp(r'^\d{10}$', message="El número debe tener exactamente 10 dígitos.")
    ])
    email = EmailField('Email', [
        validators.DataRequired('El email es requerido'),
        validators.Email(message= 'Formato de correo no válido')
    ])
    rfc = StringField('RFC', [
        validators.DataRequired(message= 'El RFC es requerido'),
        validators.Length(min=12, max=13, message= 'Su RFC debe ser minimo 12 y maximo 13 caracteres')
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message= 'La dirección es requerida')
    ])
    categoria_proveedor = SelectField('Categoria del proveedor', [
        validators.DataRequired(message= 'Debes seleccionar una categoría')
    ], coerce = int)


class CrearComboForm(FlaskForm):
    nombre_combo = StringField('Nombre del Combo', [
        validators.DataRequired(message='El nombre es obligatorio'),
        validators.Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')
    ])
    precio_combo = FloatField('Precio ($)', [
        validators.DataRequired(message='El precio es obligatorio'),
        validators.NumberRange(min=1, message='El precio debe ser mayor a 0')
    ])

class VincularComboForm(FlaskForm):
    id_padre = SelectField('Combo Base', coerce=int, validators=[
        validators.DataRequired(message='Debes seleccionar un combo base')
    ])
    id_hijo = SelectField('Ingrediente Físico', coerce=int, validators=[
        validators.DataRequired(message='Debes seleccionar un ingrediente')
    ])
    cantidad = IntegerField('Cantidad', [
        validators.DataRequired(message='La cantidad es obligatoria'),
        validators.NumberRange(min=1, message='La cantidad mínima es 1')
    ])


class CreateInsumoForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.Length(min=3, max=50, message='El nombre debe tener entre 3 y 50 carácteres')
    ])
    id_unidad_medida = SelectField('Unidad de Medida', [
        validators.DataRequired(message='La unidad de medida es requerida'),
        validators.NumberRange(min=1, message='Debes seleccionar una unidad válida')
    ], coerce=int)
    costo_unitario = DecimalField('Costo Unitario', [
        validators.DataRequired(message='El costo es requerido'),
        validators.NumberRange(min=0, message='El costo unitario no puede ser negativo')
    ])
    porcentaje_merma = DecimalField('Porcentaje Merma', [
        validators.DataRequired(message='El porcentaje de merma es requerido'),
        validators.NumberRange(min=0, message='La merma no puede ser negativa')
    ])

class EditInsumoForm(CreateInsumoForm):
    id_insumo = StringField('ID Insumo', [
        validators.DataRequired(message='El ID es requerido')
    ])
    id_unidad_medida = SelectField('Unidad de Medida', [
        validators.DataRequired(message='La unidad de medida es requerida'),
        validators.NumberRange(min=1, message='Debes seleccionar una unidad válida')
    ], coerce=int)
    costo_unitario = DecimalField('Costo Unitario', [
        validators.DataRequired(message='El costo es requerido')
    ])
    porcentaje_merma = DecimalField('Porcentaje Merma', [
        validators.DataRequired(message='El porcentaje de merma es requerido')
    ])
    activo = SelectField('Activo', [
        validators.Optional()
    ], choices=[(1, 'Activo'), (0, 'Inactivo')], coerce=int)

class EliminarInsumoForm(Form):
    id_insumo = StringField('ID Insumo', [
        validators.DataRequired(message='El ID es requerido')
    ])

class CompraForm(Form):
    id_proveedor = SelectField('Proveedor', [
        validators.DataRequired(message='El proveedor es requerido'),
        validators.NumberRange(min=1, message='Debes seleccionar un proveedor')
    ], coerce=int)
    

class DetalleCompraForm(Form):
    id_compra = StringField('ID Compra', [
        validators.DataRequired(message='El ID es requerido')
    ])
    id_insumo = StringField('ID Insumo', [
        validators.DataRequired(message='El ID es requerido')
    ])
    cantidad = DecimalField('Cantidad', [
        validators.DataRequired(message='La cantidad es requerida')
    ])
    precio_unitario = DecimalField('Precio Unitario', [
        validators.DataRequired(message='El precio unitario es requerido')
    ])

class EliminarCompraForm(Form):
    id_compra = StringField('ID Compra', [
        validators.DataRequired(message='El ID es requerido')
    ])

class ActualizarCompraForm(Form):
    id_compra = StringField('ID Compra', [
        validators.DataRequired(message='El ID es requerido')
    ])
    id_proveedor = SelectField('Proveedor', [
        validators.DataRequired(message='El proveedor es requerido'),
        validators.NumberRange(min=1, message='Debes seleccionar un proveedor')
    ], coerce=int)
    id_insumo = SelectField('Insumo', [
        validators.DataRequired(message='El insumo es requerido'),
        validators.NumberRange(min=1, message='Debes seleccionar un insumo')
    ], coerce=int)
    cantidad = DecimalField('Cantidad', [
        validators.DataRequired(message='La cantidad es requerida')
    ])
    precio_unitario = DecimalField('Precio Unitario', [
        validators.DataRequired(message='El precio unitario es requerido')
    ])
    fecha_compra = DateField('Fecha de Compra', [
        validators.DataRequired(message='La fecha de compra es requerida')
    ])
    estado_compra = SelectField('Estado de Compra', [
        validators.DataRequired(message='El estado de la compra es requerido')
    ], coerce=str)

class ComboForm(FlaskForm):
    nombre = StringField('Nombre del Combo', validators=[
        validators.DataRequired(message='El nombre es obligatorio'),
        validators.Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')
    ])
    descripcion = StringField('Descripción', validators=[
        validators.Optional(),
        validators.Length(max=255, message='La descripción no puede exceder los 255 caracteres')
    ])
    precio_venta = DecimalField('Precio de Venta ($)', validators=[
        validators.DataRequired(message='El precio es obligatorio'),
        validators.NumberRange(min=0.01, message='El precio debe ser mayor a 0')
    ])


class CategoriaProveedorForm(Form):
    nombre = StringField('Nombre de la categoria', [
        validators.DataRequired(message='El nombre de la categoria es requerida')
    ])

class ProveedorForm(Form):
    nombre_empresa = StringField('Nombre de empresa', [
        validators.DataRequired(message = 'El nombdre de empresa es requerida')
    ])

    nombre_contacto = StringField('Nombre del contacto', [
        validators.DataRequired(message='El nombre del contacto es requerido')
    ])

    apellido_pa = StringField('Apellido Paterno', [
        validators.DataRequired(message='El apellido paterno es requerido')
    ])

    apellido_ma = StringField('Apellido Materno', [
        validators.DataRequired(message='El apellido materno es requerido')
    ])

    telefono = TelField('Teléfono', [
        validators.DataRequired(message= 'El Teléfono es requerido'),
        validators.length(min=10, message='El número debe tener 10 digitos'),
        validators.Regexp(r'^\d{10}$', message="El número debe tener exactamente 10 dígitos.")
    ])

    email = EmailField('Email', [
        validators.DataRequired('El email es requerido'),
        validators.Email(message= 'Formato de correo no válido')
    ])

    rfc = StringField('RFC', [
        validators.DataRequired(message= 'El RFC es requerido'),
        validators.length(min=12, max=13, message= 'Su RFC debe ser minimo 12 y maximo 13 caracteres')
    ])

    direccion = StringField('Dirección', [
        validators.DataRequired(message= 'La dirección es requerida')
    ])

    categoria_proveedor = SelectField('Categoria del proveedor', [
        validators.DataRequired(message= 'Debes seleccionar una categoría'),
        validators.NumberRange(min=1, message='Debes seleccionar una categoría')
    ], coerce = int)
    
class VentasForm(Form):
    metodo_pago = SelectField('Método de pago', [
        validators.DataRequired(message='Debes seleccionar un método de pago')
    ], coerce=str)

    numero_cuenta = StringField(
        'Número de cuenta', [
            validators.Optional(),
            validators.Length(min=16, max=20, message='El Num. cuenta debe tener entre 16 a 20 digitos'),
            validators.Regexp(regex=r'^\d+$', message='El Num. cuenta solo debe contener números, sin espacios ni letra')
        ], render_kw={"minlenght": 16, "maxlenght":20, "pattern":"[0-9]*", "inputmode":"numeric"})

    pin = IntegerField(
        'PIN tarjeta', [
            validators.Optional()
        ])

    monto_recibido = FloatField(
        'Monto recibido',[
            validators.Optional(),
            validators.NumberRange(min=0.01, message='Debe ingresar un monto recibido válido')
        ])

class MermaForm(FlaskForm):
    id_lote = HiddenField('ID Lote', [validators.DataRequired()])
    id_insumo = HiddenField('ID Insumo', [validators.DataRequired()])
    cantidad = DecimalField('Cantidad a retirar', [
        validators.DataRequired(message='La cantidad es requerida'),
        validators.NumberRange(message='La cantidad debe ser mayor a 0')
    ])
    motivo = StringField('Motivo', [
        validators.DataRequired(message='El motivo es requerido'),
        validators.Length(max=255, message='El motivo no puede exceder los 255 caracteres')
    ])

class SalidaEfectivoForm(Form):
    monto = DecimalField('Monto a retirar', [
        validators.DataRequired(message='El monto es obligatorio'),
        validators.NumberRange(min=0.10, message='El monto debe ser mayor a cero')
    ])

    motivo = StringField('Motivo de la salida', [
        validators.DataRequired('Debes especificar el motivo'),
        validators.Length(min=5, max=255, message='El motivo debe tener entre 5 a 255 caracteres')
    ])

class SolicitudProduccionVentasForm(Form):
    id_producto = HiddenField('id_producto', [
        validators.DataRequired()
    ])

    cantidad = IntegerField('Cantidad a solicitar', [
        validators.DataRequired(message= 'La cantidad es requerida'),
        validators.NumberRange(min=1, message='Debes solicitar al menos 1 unidad')
    ])

class FiltroFechaForm(Form):
    class Meta:
        csrf = False # Lo desactivamos por que es un formulario de búsqueda
    
    fecha = DateField('Fecha', [
        validators.Optional()
    ])

    submit = SubmitField('Filtrar')


# ==========================================================================    
    # ==========================================================================
# FORMULARIOS DE ADMINISTRACIÓN (USUARIOS)
# ==========================================================================

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido_pa = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_ma = StringField('Apellido Materno')
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    telefono = TelField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message="La contraseña debe tener mayúscula, minúscula, número y carácter especial.")
    ])
    rol_id = SelectField('Rol', coerce=int, validators=[DataRequired()])

# ==========================================================================
# FORMULARIOS DE RECETAS
# ==========================================================================

class RecetaFiltroForm(FlaskForm):
    search = StringField('Buscar', validators=[Optional()])

class RecetaInsumoForm(FlaskForm):
    id_producto = HiddenField('ID Producto', validators=[DataRequired()])
    id_insumo = SelectField('Insumo', coerce=int, validators=[DataRequired()])
    cantidad_requerida = DecimalField('Cantidad Requerida', 
        validators=[DataRequired(), NumberRange(min=0.01, message="La cantidad debe ser mayor a 0")],
        places=4)

class ProduccionOrdenForm(FlaskForm):
    id_producto = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad_programada = IntegerField('Cantidad a producir', 
        validators=[DataRequired(), NumberRange(min=1, message="La cantidad debe ser al menos 1")])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])

class ProduccionFinalizarForm(FlaskForm):
    cantidad_producida = IntegerField('Cantidad producida', 
        validators=[DataRequired(), NumberRange(min=1, message="La cantidad debe ser al menos 1")])

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    precio_venta = DecimalField('Precio de Venta', validators=[DataRequired(), NumberRange(min=0)])
    id_categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    imagen = FileField('Imagen del Producto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], '¡Solo se permiten imágenes (jpg, png)!')
    ])
    submit = SubmitField('Crear Producto y Continuar a Receta')
