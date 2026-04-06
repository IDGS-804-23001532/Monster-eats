from flask_wtf import FlaskForm
from wtforms import Form, SelectField, DecimalField, HiddenField, EmailField, PasswordField, StringField, DateField, TelField, IntegerField, FloatField
from wtforms import validators

class LoginForm(Form):
    email = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Formato de correo no válido')
    ])

    password = PasswordField('Password', [
        validators.DataRequired(message='El password es requerido'),
        validators.Length(min=8, message='El password debe tener al menos 8 carácteres')
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
        validators.regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.')
    ])

class CreateInsumoForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.Length(min=3, max=50, message='El nombre debe tener entre 3 y 50 carácteres')
    ])
    id_unidad_medida = SelectField('Unidad de Medida', [
        validators.DataRequired(message='La unidad de medida es requerida')
    ], coerce=int)
    costo_unitario = DecimalField('Costo Unitario', [
        validators.DataRequired(message='El costo es requerido')
    ])
    porcentaje_merma = DecimalField('Porcentaje Merma', [
        validators.DataRequired(message='El porcentaje de merma es requerido')
    ])

class EditInsumoForm(CreateInsumoForm):
    id_insumo = StringField('ID Insumo', [
        validators.DataRequired(message='El ID es requerido')
    ])
    id_unidad_medida = SelectField('Unidad de Medida', [
        validators.DataRequired(message='La unidad de medida es requerida')
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
        validators.DataRequired(message='El proveedor es requerido')
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
        validators.DataRequired(message='El proveedor es requerido')
    ], coerce=int)
    id_insumo = SelectField('Insumo', [
        validators.DataRequired(message='El insumo es requerido')
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
        validators.DataRequired(message= 'Debes seleccionar una categoría')
    ], coerce = int)

class VentasForm(Form):
    metodo_pago = SelectField('Método de pago', [
        validators.DataRequired(message='Debes seleccionar un método de pago')
    ], coerce=str)

    numero_cuenta = StringField(
        'Número de cuenta', [
            validators.Optional()
        ])

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
