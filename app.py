import configparser
import sys

# PARCHE PARA PYTHON 3.13
# Engañamos a las librerías viejas para que encuentren lo que buscan
if not hasattr(configparser, 'SafeConfigParser'):
    configparser.SafeConfigParser = configparser.ConfigParser

try:
    import pkg_resources
except ImportError:
    # Si aun así no lo encuentra, creamos un objeto vacío para que no truene el import
    class MockPkgResources:
        def get_distribution(self, name): return None
    sys.modules['pkg_resources'] = MockPkgResources()

from flask import Flask, render_template, redirect, url_for, flash
from flask import session
from extensions import limiter, mail
from flask_wtf.csrf import CSRFProtect, CSRFError
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
from combos.routes import combos
from solicitud_Produccion.routes import solicitud_produccion
from tablero_kds.routes import tablero_kds
from costo_Utilidad.routes import costo_utilidad
from tablero_kds.routes import tablero_kds
from recetas import recetas_bp as recetas
from produccion import produccion_bp as produccion
from usuarios import usuarios_bp as usuarios
from Pagina import pagina_bp
from models import db, Usuario, Rol
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.decorators import roles_required
from datetime import timedelta
from jinja2 import TemplateError
from models import db

app = Flask(__name__)

limiter.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app, db)
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
mail.init_app(app)

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
app.register_blueprint(combos)
app.register_blueprint(solicitud_produccion)
app.register_blueprint(costo_utilidad)
app.register_blueprint(tablero_kds)
app.register_blueprint(recetas, url_prefix='/recetas')
app.register_blueprint(produccion, url_prefix='/produccion')
app.register_blueprint(usuarios, url_prefix='/usuarios')
app.register_blueprint(pagina_bp)


@app.context_processor
def inject_cart_count():
    """Provee `cart_count` a todas las plantillas para mostrar badge en el header.
    Para usuarios no autenticados usa la sesión; para autenticados intenta leer
    el resumen desde la vista `vw_carrito_resumen` (si existe).
    """
    try:
        from flask_security import current_user
        count = 0
        # Preferir carrito en sesión si existe
        sess_cart = session.get('carrito')
        if sess_cart is not None:
            count = sum(item.get('cantidad', 1) for item in sess_cart)
        elif current_user.is_authenticated:
            # Intentar consultar la vista de resumen (respaldo para el módulo ventas)
            try:
                resumen = db.session.execute(db.text("SELECT total_piezas FROM vw_carrito_resumen WHERE id_usuario = :id_usuario LIMIT 1"), {'id_usuario': current_user.id_usuario}).mappings().first()
                if resumen and resumen.get('total_piezas') is not None:
                    count = int(resumen.get('total_piezas'))
            except Exception:
                count = 0
        return dict(cart_count=count)
    except Exception:
        return dict(cart_count=0)


@app.route("/")
def inicio():
    from models import Producto, Combo, CategoriaProducto
    
    cat_hambur = CategoriaProducto.query.filter(CategoriaProducto.nombre.ilike('Hamburguesas')).first()
    producto_hambur = Producto.query.filter_by(id_categoria=cat_hambur.id_categoria, activo=True).first() if cat_hambur else None
    
    cat_papas = CategoriaProducto.query.filter(CategoriaProducto.nombre.ilike('Papas')).first()
    producto_papa = Producto.query.filter_by(id_categoria=cat_papas.id_categoria, activo=True).first() if cat_papas else None
    
    combo_destacado = Combo.query.filter_by(activo=True).first()
    
    return render_template('inicio.html', producto_hambur=producto_hambur, producto_papa=producto_papa, combo_destacado=combo_destacado)

@app.route("/bienvenida")
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

@app.errorhandler(TemplateError)
def handle_template_error(e):
    # Intercepta errores de diseño para enviar a la ventana 500
    return render_template('500.html'), 500 

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    # Limpiamos cualquier dato residual de la sesión por seguridad
    session.clear()
    flash('Tu sesión expiró o no tienes permiso para realizar esta acción. Por favor, inicia sesión nuevamente.', 'error')
    return redirect(url_for('auth.login'))
 
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html', error_description=e.description), 429

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)