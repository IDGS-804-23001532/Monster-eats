from wtforms import Form, SelectField, DecimalField
from wtforms import EmailField, PasswordField, StringField, DateField, TelField
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
        validators.Length(min = 10, message='Minimo son 8 digitos númericos'),
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