from wtforms import Form
from wtforms import EmailField, PasswordField, StringField, DateField, TelField, SelectField, IntegerField, FloatField, DecimalField, HiddenField, SubmitField
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

