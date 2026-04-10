from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, func
from flask_security import UserMixin, RoleMixin
import datetime

db = SQLAlchemy()

# Modulo de Usuarios y Roles
usuarios_roles = db.Table('usuarios_roles',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id_usuario')),
    db.Column('id_rol', db.Integer, db.ForeignKey('roles.id_rol'))
)

class Rol(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True) # Se debe llamar 'name'
    descripcion = db.Column(db.String(100), nullable=False)

class Persona(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_pa = db.Column(db.String(50), nullable=False)
    apellido_ma = db.Column(db.String(50), nullable=True) 
    fecha_nac = db.Column(db.Date, nullable=True)
    telefono = db.Column(db.String(16), nullable=True)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), nullable=False, unique=True)
    
    # Campos OBLIGATORIOS de Flask-Security
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    
    fecha_registro = db.Column(db.DateTime, nullable=False, default=func.now())
    bloqueado_hasta = db.Column(db.DateTime, nullable=True)
    intentos_fallidos = db.Column(db.Integer, nullable=False, default=0)

    # Relaciones
    persona = db.relationship('Persona', backref='usuario', lazy=True)
    roles = db.relationship('Rol', secondary=usuarios_roles, backref=db.backref('usuarios', lazy='dynamic'))

# ==========================================================================
# MÓDULO DE PROVEEDORES
# ==========================================================================

class CategoriaProveedor(db.Model):
    __tablename__ = 'categorias_proveedor'
    id_categoria_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    
    proveedores = db.relationship('Proveedor', backref='categoria', lazy=True)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_empresa = db.Column(db.String(100), nullable=False, unique=True, index=True)
    nombre_contacto = db.Column(db.String(50), nullable=False)
    apellido_pa = db.Column(db.String(50), nullable=False)
    apellido_ma = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    rfc = db.Column(db.String(15), unique=True, nullable=True)
    direccion = db.Column(db.String(255), nullable=False)
    id_categoria_proveedor = db.Column(db.Integer, db.ForeignKey('categorias_proveedor.id_categoria_proveedor'), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=func.now())
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)
# ==========================================================================
# MÓDULO DE COMPRAS
# ==========================================================================

class Compra(db.Model):
    __tablename__ = 'compras'
    id_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_compra = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    estado_compra = db.Column(db.Enum('Completada', 'Cancelada', name='estado_compra_enum'), nullable=False, default='Completada', index=True)

    # Relaciones
    proveedor = db.relationship('Proveedor', backref='compras', lazy=True)
    usuario = db.relationship('Usuario', backref='compras', lazy=True)
    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True)
    __table_args__ = (
        CheckConstraint('total >= 0', name='chk_compras_total'),
    )

class ConversionUnidadInsumo(db.Model):
    __tablename__ = 'conversion_unidades_insumo'
    id_conversion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    id_unidad_compra = db.Column(db.Integer, db.ForeignKey('unidades_medida.id_unidad_medida'), nullable=False)
    cantidad_equivalente_base = db.Column(db.Numeric(12, 4), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint('cantidad_equivalente_base > 0', name='chk_conversion_equivalencia'),
        UniqueConstraint('id_insumo', 'id_unidad_compra', name='uq_conversion_insumo_unidad'),
    )


# ==========================================================================
# MÓDULO DE INVENTARIO DE MATERIA PRIMA
# ==========================================================================

class UnidadMedida(db.Model):
    __tablename__ = 'unidades_medida'
    id_unidad_medida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)
    abreviatura = db.Column(db.String(10), nullable=False, unique=True)

class Insumo(db.Model):
    __tablename__ = 'insumos'
    id_insumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True, index=True)
    id_unidad_medida = db.Column(db.Integer, db.ForeignKey('unidades_medida.id_unidad_medida'), nullable=False)
    costo_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    # fecha_cad = db.Column(db.Date, nullable=True)
    # nivel_min_reorden = db.Column(db.Numeric(10, 4), nullable=True)
    porcentaje_merma = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Relaciones
    unidad_medida = db.relationship('UnidadMedida', backref='insumos', lazy=True)

    __table_args__ = (
        CheckConstraint('costo_unitario >= 0', name='chk_insumos_costo_unitario'),
        # CheckConstraint('nivel_min_reorden IS NULL OR nivel_min_reorden >= 0', name='chk_insumos_nivel_min_reorden'),
        CheckConstraint('porcentaje_merma >= 0 AND porcentaje_merma <= 100', name='chk_insumos_porcentaje_merma'),
    )

# ==========================================================================
# MÓDULO DE DETALLE DE COMPRAS
# ==========================================================================
class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compras'
    id_detalle_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compras.id_compra'), nullable=False)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    cantidad_comprada = db.Column(db.Numeric(10, 4), nullable=False)
    id_unidad_medida = db.Column(db.Integer, db.ForeignKey('unidades_medida.id_unidad_medida'), nullable=False)
    costo_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    # Nota: SQLAlchemy no maneja columnas "GENERATED ALWAYS" nativamente de forma sencilla
    # Lo ideal es calcularlo en la lógica de negocio antes de guardar
    costo_subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    # Relaciones
    insumo = db.relationship('Insumo', backref='detalle_compras', lazy=True)
    unidad_medida = db.relationship('UnidadMedida', backref='detalle_compras', lazy=True)

    __table_args__ = (
        CheckConstraint('cantidad_comprada > 0', name='chk_detalle_compras_cantidad'),
        CheckConstraint('costo_unitario >= 0', name='chk_detalle_compras_costo'),
        UniqueConstraint('id_compra', 'id_insumo', name='uq_detalle_compras'),
    )
# ==========================================================================
# MÓDULO DE INVENTARIO DE MATERIA PRIMA - LOTE INSUMO
# ==========================================================================
class LoteInsumo(db.Model):
    __tablename__ = 'lotes_insumo'
    id_lote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    id_detalle_compra = db.Column(db.Integer, db.ForeignKey('detalle_compras.id_detalle_compra'), nullable=True)
    cantidad_inicial = db.Column(db.Numeric(10, 4), nullable=False)
    cantidad_disponible = db.Column(db.Numeric(10, 4), nullable=False)
    fecha_caducidad = db.Column(db.Date, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=func.now())

    # Relaciones
    insumo = db.relationship('Insumo', backref='lotes', lazy=True)
    __table_args__ = (
        CheckConstraint('cantidad_inicial >= 0', name='chk_lotes_insumo_cantidad_inicial'),
        CheckConstraint('cantidad_disponible >= 0', name='chk_lotes_insumo_cantidad_disponible'),
        CheckConstraint('cantidad_disponible <= cantidad_inicial', name='chk_lotes_insumo_cantidad_valida'),
    )

# ==========================================================================
# MÓDULO DE INVENTARIO DE MATERIA PRIMA - INVENTARIO INSUMO
# ==========================================================================

class InventarioInsumo(db.Model):
    __tablename__ = 'inventario_insumos'
    id_inventario_insumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_lote = db.Column(db.Integer, db.ForeignKey('lotes_insumo.id_lote'), nullable=False)
    nivel_minimo = db.Column(db.Numeric(10, 4), nullable=True)
    ubicacion_pasillo = db.Column(db.String(50), nullable=True)

    __table_args__ = (
        CheckConstraint('nivel_minimo IS NULL OR nivel_minimo >= 0', name='chk_inventario_insumos_nivel'),
        UniqueConstraint('id_lote', name='uq_inventario_insumos_lote'),
    )

class MermaLog(db.Model):
    __tablename__ = 'mermas_log'
    id_merma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 4), nullable=False)
    fecha_baja = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)
    motivo = db.Column(db.String(255), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_lote = db.Column(db.Integer, db.ForeignKey('lotes_insumo.id_lote'), nullable=True)

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_mermas_cantidad'),
    )

class HistorialPrecioInsumo(db.Model):
    __tablename__ = 'historial_precios_insumos'
    id_historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    precio_anterior = db.Column(db.Numeric(10, 2), nullable=True)
    precio_nuevo = db.Column(db.Numeric(10, 2), nullable=True)
    accion = db.Column(db.Enum('NUEVO', 'MODIFICACION', 'ELIMINADO', name='accion_enum'), nullable=False)
    fecha_cambio = db.Column(db.DateTime, nullable=False, default=func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)

class MovimientoInventarioInsumo(db.Model):
    __tablename__ = 'movimientos_inventario_insumos'
    id_movimiento_insumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    tipo_movimiento = db.Column(db.Enum('ENTRADA_COMPRA', 'SALIDA_PRODUCCION', 'SALIDA_MERMA', 'AJUSTE_MANUAL', 'REVERSO_COMPRA', name='tipo_mov_insumo_enum'), nullable=False, index=True)
    cantidad = db.Column(db.Numeric(12, 4), nullable=False)
    stock_anterior = db.Column(db.Numeric(12, 4), nullable=False)
    stock_nuevo = db.Column(db.Numeric(12, 4), nullable=False)
    referencia_tabla = db.Column(db.String(50), nullable=True)
    referencia_id = db.Column(db.Integer, nullable=True)
    motivo = db.Column(db.String(255), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_lote = db.Column(db.Integer, db.ForeignKey('lotes_insumo.id_lote'), nullable=True)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_mov_insumo_cantidad'),
        CheckConstraint('stock_anterior >= 0', name='chk_mov_insumo_stock_anterior'),
        CheckConstraint('stock_nuevo >= 0', name='chk_mov_insumo_stock_nuevo'),
    )


# ==========================================================================
# MÓDULO DE RECETAS
# ==========================================================================

class CategoriaProducto(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False, unique=True, index=True)
    imagen = db.Column(db.String(255), nullable=True, default='default_product.png')
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    __table_args__ = (
        CheckConstraint('precio_venta >= 0', name='chk_productos_precio'),
    )

class Receta(db.Model):
    __tablename__ = 'recetas'
    id_receta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    cantidad_requerida = db.Column(db.Numeric(10, 4), nullable=False)

    __table_args__ = (
        CheckConstraint('cantidad_requerida > 0', name='chk_recetas_cantidad'),
        UniqueConstraint('id_producto', 'id_insumo', name='uq_recetas'),
    )

# ==========================================================================
# MÓDULO DE PRODUCCIÓN Y SOLICITUDES
# ==========================================================================

class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'
    id_orden_produccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_usuario_crea = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_usuario_responsable = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    cantidad_programada = db.Column(db.Integer, nullable=False)
    cantidad_producida = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.Enum('Pendiente', 'En Proceso', 'Completada', 'Cancelada', name='estado_op_enum'), nullable=False, default='Pendiente', index=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_finalizacion = db.Column(db.DateTime, nullable=True)
    observaciones = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        CheckConstraint('cantidad_programada > 0', name='chk_op_cantidad_programada'),
        CheckConstraint('cantidad_producida >= 0', name='chk_op_cantidad_producida'),
    )

class SolicitudProduccion(db.Model):
    __tablename__ = 'solicitudes_produccion'
    id_solicitud_prod = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario_solicita = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_orden_produccion = db.Column(db.Integer, db.ForeignKey('ordenes_produccion.id_orden_produccion'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Enum('Pendiente', 'En Proceso', 'Completada', 'Cancelada', name='estado_sol_enum'), nullable=False, default='Pendiente', index=True)
    fecha_solicitud = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)
    fecha_completada = db.Column(db.DateTime, nullable=True)
    numero_orden = db.Column(db.String(20), nullable=True)

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_solicitudes_cantidad'),
    )

# ==========================================================================
# MÓDULO DE INVENTARIO DE PRODUCTOS TERMINADOS
# ==========================================================================

class InventarioProducto(db.Model):
    __tablename__ = 'inventario_productos'
    id_inventario_prod = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False, unique=True)
    stock_actual = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint('stock_actual >= 0', name='chk_inventario_productos_stock'),
    )

class Combo(db.Model):
    __tablename__ = 'combos'
    id_combo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto_padre = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_producto_hijo = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint('cantidad >= 1', name='chk_combos_cantidad'),
        CheckConstraint('id_producto_padre <> id_producto_hijo', name='chk_combos_distintos'),
        UniqueConstraint('id_producto_padre', 'id_producto_hijo', name='uq_combos'),
    )

class MovimientoInventarioProducto(db.Model):
    __tablename__ = 'movimientos_inventario_productos'
    id_movimiento_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    tipo_movimiento = db.Column(db.Enum('ENTRADA_PRODUCCION', 'SALIDA_VENTA', 'SALIDA_COMBO', 'REVERSO_VENTA', 'AJUSTE_MANUAL', name='tipo_mov_prod_enum'), nullable=False, index=True)
    cantidad = db.Column(db.Integer, nullable=False)
    stock_anterior = db.Column(db.Integer, nullable=False)
    stock_nuevo = db.Column(db.Integer, nullable=False)
    referencia_tabla = db.Column(db.String(50), nullable=True)
    referencia_id = db.Column(db.Integer, nullable=True)
    motivo = db.Column(db.String(255), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_mov_prod_cantidad'),
        CheckConstraint('stock_anterior >= 0', name='chk_mov_prod_stock_anterior'),
        CheckConstraint('stock_nuevo >= 0', name='chk_mov_prod_stock_nuevo'),
    )

# ==========================================================================
# MÓDULO DE VENTAS Y CAJA
# ==========================================================================

class MetodoPago(db.Model):
    __tablename__ = 'metodos_pago'
    id_metodo_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)

class Venta(db.Model):
    __tablename__ = 'ventas'
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_venta = db.Column(db.DateTime, nullable=False, default=func.now(), index=True)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodos_pago.id_metodo_pago'), nullable=False)
    referencia_pago = db.Column(db.String(50), nullable=True)
    estado_venta = db.Column(db.Enum('Pendiente', 'Pagado', 'Cancelado', name='estado_venta_enum'), nullable=False, default='Pendiente', index=True)

    __table_args__ = (
        CheckConstraint('total >= 0', name='chk_ventas_total'),
    )

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    # Al igual que en compras, el subtotal lo calcularás antes de guardar el modelo
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_detalle_ventas_cantidad'),
        CheckConstraint('precio_unitario >= 0', name='chk_detalle_ventas_precio'),
        UniqueConstraint('id_venta', 'id_producto', name='uq_detalle_ventas'),
    )

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id_ticket = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False, unique=True)
    folio = db.Column(db.String(20), nullable=False, unique=True)
    fecha_emision = db.Column(db.DateTime, nullable=False, default=func.now())
    monto_pagado = db.Column(db.Numeric(10, 2), nullable=False)
    leyenda = db.Column(db.String(255), nullable=False, default='Gracias por comprar, pase por su producto en el mostrador')

    __table_args__ = (
        CheckConstraint('monto_pagado >= 0', name='chk_tickets_monto'),
    )

class SalidaEfectivo(db.Model):
    __tablename__ = 'salidas_efectivo'
    id_salida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False, default=func.now())

    __table_args__ = (
        CheckConstraint('monto > 0', name='chk_salidas_monto'),
    )

# ==========================================================================
# MÓDULO DE CUENTAS (SIMULACIÓN DE TARJETAS)
# ==========================================================================

class Cuenta(db.Model):
    __tablename__ = 'cuenta'
    id_cuenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False, unique=True)
    num_cuenta = db.Column(db.String(20), nullable=False, unique=True)
    pin = db.Column(db.String(4), nullable=False)
    saldo = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint('saldo >= 0', name='chk_cuenta_saldo'),
    )

class MovimientoCuenta(db.Model):
    __tablename__ = 'movimientos_cuenta'
    id_movimiento_cuenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuenta.id_cuenta'), nullable=False)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=True)
    tipo_movimiento = db.Column(db.Enum('ABONO', 'CARGO', 'REVERSO', 'AJUSTE', name='tipo_mov_cuenta_enum'), nullable=False)
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    saldo_anterior = db.Column(db.Numeric(12, 2), nullable=False)
    saldo_nuevo = db.Column(db.Numeric(12, 2), nullable=False)
    referencia = db.Column(db.String(100), nullable=True)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=func.now())

    __table_args__ = (
        CheckConstraint('monto > 0', name='chk_mov_cta_monto'),
        CheckConstraint('saldo_anterior >= 0', name='chk_mov_cta_saldo_anterior'),
        CheckConstraint('saldo_nuevo >= 0', name='chk_mov_cta_saldo_nuevo'),
    )