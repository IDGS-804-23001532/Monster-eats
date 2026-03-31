from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ---------------------------------------------------------
# MÓDULO: USUARIOS
# ---------------------------------------------------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_pa = db.Column(db.String(50), nullable=False)
    apellido_ma = db.Column(db.String(50), nullable=False)
    fecha_nac = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Guardaremos el HASH
    rol = db.Column(db.String(20), nullable=False) # Gerente, Cocina, Caja
    estatus = db.Column(db.Integer, default=1) # 1 para Activo, 0 para Baja Lógica

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# ---------------------------------------------------------
# MÓDULO: RECETAS (Fichas Técnicas)
# ---------------------------------------------------------
class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre_platillo = db.Column(db.String(100), nullable=False) # Ej: Monster Burger
    descripcion = db.Column(db.Text)
    precio_venta = db.Column(db.Float, nullable=False)
    # Relación con los detalles de la receta (ingredientes)
    detalles = db.relationship('RecetaDetalle', backref='receta', lazy=True)

class RecetaDetalle(db.Model):
    __tablename__ = 'recetas_detalles'
    id = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False) # Viene de Inventario
    cantidad_requerida = db.Column(db.Float, nullable=False) # Ej: 0.150 (para 150g)

# ---------------------------------------------------------
# MÓDULO: PRODUCCIÓN
# ---------------------------------------------------------
class Produccion(db.Model):
    __tablename__ = 'produccion'
    id = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # El cocinero
    cantidad_a_producir = db.Column(db.Integer, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.now)
    estatus = db.Column(db.String(20), default='Pendiente') # Pendiente, En Proceso, Finalizada
    
# Nota: Para que esto funcione, necesitas que tus compañeros 
# ya tengan el modelo de 'Insumos' (Inventario) creado:
class Insumo(db.Model):
    __tablename__ = 'insumos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    stock_actual = db.Column(db.Float)
    costo_unitario = db.Column(db.Float)
    unidad_medida = db.Column(db.String(10)) # g, ml, pza 