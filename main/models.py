from api import db

client_orders = db.Table('clientes_pedidos',
    db.Column('cliente_pedido_id', db.Integer, primary_key=True),
    db.Column('cliente_id_foreign', db.Integer, db.ForeignKey('clientes.cliente_id_pkey')),
    db.Column('pedidos_id_foreign', db.Integer, db.ForeignKey('pedidos.pedido_id_pkey'))
)

product_orders = db.Table('productos_pedidos',
    db.Column('productos_pedidos_id', db.Integer, primary_key=True),
    db.Column('productos_id_foreign', db.Integer, db.ForeignKey('productos.producto_id_pkey')),
    db.Column('pedidos_id_foreign', db.Integer, db.ForeignKey('pedidos.pedido_id_pkey'))
)

class Users(db.Model):

    __tablename__ = "usuarios"

    usuario_cedula_pkey = db.Column(db.String(9), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(8), unique=True, nullable=False)
    contraseña = db.Column(db.String(12), nullable=False)
    estado = db.Column(db.Boolean, default=True)

    tipo_de_usuario_foreign = db.Column(
        db.Integer,
        db.ForeignKey('tipos_de_usuario.tipo_de_usuario_pkey')
    )

class TypeOfUsers(db.Model):

    __tablename__ = "tipos_de_usuario"

    tipo_de_usuario_pkey = db.Column(db.Integer, primary_key=True)
    nombre_del_tipo = db.Column(db.String(100), unique=True, nullable=True)

    tipos_de_usuario = db.relationship(
        'Users', 
        backref='usuarios', 
        lazy=True
    )

class Expenses(db.Model):

    __tablename__ = "egresos"

    egreso_id_pkey = db.Column(db.Integer, primary_key=True)
    fecha_egreso = db.Column(db.Date, nullable=False)
    material = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    proveedor = db.Column(db.String(200), nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float(4, 2))

class Incomes(db.Model):

    __tablename__ = "ingresos"

    id_ingreso_pkey = db.Column(db.Integer, primary_key=True)
    monto_ingreso = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

class Clients(db.Model):

    __tablename__ = "clientes"

    cliente_id_pkey = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(8), nullable=False, unique=True)

    direccion_id_foreign = db.Column(db.Integer, db.ForeignKey('direcciones.direccion_id_pkey'))
    
    pedidos = db.relationship('Orders', 
        secondary=client_orders, backref=db.backref('pedidos', lazy='dynamic'),lazy='dynamic')

class Directions(db.Model):

    __tablename__ = "direcciones"

    direccion_id_pkey = db.Column(db.Integer, primary_key=True)
    ciudad = db.Column(db.String(200), nullable=False)
    barrio = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)

    clientes = db.relationship(
        'Clients',
        backref=db.backref('clientes'),
        lazy=True
    )

class Orders(db.Model):

    __tablename__ = "pedidos"

    pedido_id_pkey = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.Date, nullable=False)
    metodo_de_pago = db.Column(db.String(100), nullable=False)

    tipo_de_entrega = db.Column(
        db.Integer,
        db.ForeignKey('tipos_de_entrega.tipo_de_entrega_id_pkey')
    )

    productos = db.relationship('Products', 
        secondary=product_orders, backref=db.backref('productos', lazy='dynamic'),lazy='dynamic')

class Products(db.Model):

    __tablename__ = "productos"

    producto_id_pkey = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    siglas = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.Integer, nullable=False)

class TypesOfDelivery(db.Model):

    __tablename__ = "tipos_de_entrega"

    tipo_de_entrega_id_pkey = db.Column(db.Integer, primary_key=True)
    tipo_de_entrega = db.Column(db.String(100), nullable=False, unique=True)
    costo_adicional = db.Column(db.Integer, nullable=False)

    tipos_de_entrega = db.relationship(
        'Orders',
        backref=db.backref('tipos_de_entrega'),
        lazy=True
    )
