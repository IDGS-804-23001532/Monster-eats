from flask_wtf import FlaskForm 
from wtforms import EmailField, PasswordField, StringField, DateField, TelField, HiddenField, IntegerField, TextAreaField, SubmitField
from wtforms import SelectField, FloatField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    email = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Formato de correo no válido')
    ])

    password = PasswordField('Password', [
        validators.DataRequired(message='El password es requerido'),
        validators.Length(min=8, message='El password debe tener al menos 8 carácteres')
    ])

class RegisterForm(FlaskForm):
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