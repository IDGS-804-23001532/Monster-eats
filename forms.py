from wtforms import Form, EmailField, PasswordField, StringField, DateField, TelField, SelectField, IntegerField, FloatField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError, Optional, NumberRange
import re

# ==========================================================================
# FORMULARIOS DE ACCESO (AUTH)
# ==========================================================================

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
        validators.Length(min=10, message='Minimo son 10 digitos númericos'),
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

# ==========================================================================
# FORMULARIOS DE VENTAS
# ==========================================================================

class VentasForm(Form):
    metodo_pago = SelectField('Método de pago', [
        validators.DataRequired(message='Debes seleccionar un método de pago')
    ], coerce=str)
    numero_cuenta = StringField('Número de cuenta', [validators.Optional()])
    pin = IntegerField('PIN tarjeta', [validators.Optional()])
    monto_recibido = FloatField('Monto recibido',[
            validators.Optional(),
            validators.NumberRange(min=0.01, message='Debe ingresar un monto recibido válido')
        ])