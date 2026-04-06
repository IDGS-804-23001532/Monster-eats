from flask import Flask, render_template, redirect, url_for, flash
from extensions import limiter
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from auth import auth
from inventario.routes import inventario
from compras.routes import compras 
from dashboard import dashboard
from insumos.routes import insumos
from proveedores import proveedor
from ventas import venta
from inventario_Produccion.routes import inventario_produccion
from solicitud_Produccion.routes import solicitud_produccion
from costo_Utilidad.routes import costo_utilidad
from models import db, Usuario, Rol
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.decorators import roles_required
from datetime import timedelta

app = Flask(__name__)

limiter.init_app(app)
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)

# Salt 
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha256'
app.config['SECURITY_PASSWORD_SALT'] = 'Clave_Mons_eats#'

# Movemos los URLS por defecto de flask_security
app.config['SECURITY_LOGIN_URL'] = '/login_libreria'
app.config['SECURITY_LOGOUT_URL'] = '/logout_libreria'
app.config['SECURITY_REGISTER_URL'] = '/register_libreria'

db.init_app(app)
migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, Usuario, Rol)
seguridad_app = Security(app, user_datastore)

# Expiración por inactividad
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 60)
app.config['SESSION_COOKIE_SECURE'] = False 
app.config['SESSION_COOKIE_HTTPONLY'] = True # Evitar que el XSS robe la cookie


# Nos permite utilizar la plantilla del login propia en vez del flask_security
@app.login_manager.unauthorized_handler
def unauthorized():
    flash('Por favor, inicia sesión para acceder al sistema.')
    return redirect(url_for('auth.login'))

csrf = CSRFProtect()

# Rutas Blueprint
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(inventario)
app.register_blueprint(compras)
app.register_blueprint(insumos)
app.register_blueprint(proveedor)
app.register_blueprint(venta)
app.register_blueprint(inventario_produccion)
app.register_blueprint(solicitud_produccion)
app.register_blueprint(costo_utilidad)


@app.route("/")
@login_required
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Diego: Para que funcione esta parte, desactiva el debug a False (Modo desarrollador False)
@app.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html', error_description=e.description), 429

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)