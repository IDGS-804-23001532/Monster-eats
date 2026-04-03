from flask import Flask, render_template, redirect, url_for, flash
from extensions import limiter
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from auth import auth
from dashboard import dashboard
from models import db, Usuario, Rol
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.decorators import roles_required
from datetime import timedelta

app = Flask(__name__)

limiter.init_app(app)

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
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)
app.config['SESSION_COOKIE_SECURE'] = False 
app.config['SESSION_COOKIE_HTTPONLY'] = True # Evitar que el XSS robe la cookie


# Nos permite utilizar la plantilla del login propia en vez del flask_security
@app.login_manager.unauthorized_handler
def unauthorized():
    flash('Por favor, inicia sesión para acceder al sistema.')
    return redirect(url_for('auth.login'))

csrf = CSRFProtect()
app.register_blueprint(auth)
app.register_blueprint(dashboard)

@app.route("/")
def index():
    return render_template("dashboard/dashboard.html")

from compras.routes import  compras
from dashboard.routes import dashboard
app.register_blueprint(compras)
app.register_blueprint(dashboard)



if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)