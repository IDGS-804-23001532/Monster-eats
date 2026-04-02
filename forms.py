from wtforms import Form
from wtforms import EmailField, PasswordField, StringField, DateField, TelField, SelectField
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