from api import marshmallow


class TypeOfUsersSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'nombre_del_tipo',
        )

type_of_user_schema = TypeOfUsersSchema()
type_of_users_schema = TypeOfUsersSchema(many=True)


class UserSchema(marshmallow.Schema):
    
    class Meta:
        fields = (
            'usuario_cedula_pkey',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'correo',
            'telefono',
            'estado',
            'nombre_del_tipo'
        )
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ExpensesSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'fecha_egreso',
            'material',
            'cantidad',
            'proveedor',
            'costo',
            'peso'
        )

expense_schema = ExpensesSchema()
expenses_schema = ExpensesSchema(many=True)

class IncomesSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'monto_ingreso',
            'motivo',
            'fecha'
        )

income_schema = IncomesSchema()
incomes_schema = IncomesSchema(many=True)

class ClientsSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'nombre',
            'apellido',
            'telefono',
            'ciudad',
            'barrio',
            'direccion'
        )

client_schema = ClientsSchema()
clients_schema = ClientsSchema(many=True)

class DirectionsSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'ciudad',
            'barrio',
            'direccion'
        )

direction_schema = DirectionsSchema()
directions_schema = DirectionsSchema(many=True)

class OrdersSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'id_pedido_pkey',
        )

order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)

class ProductsSchema(marshmallow.Schema):

    class Meta:
        fields = (
            'nombre',
            'siglas',
            'precio'
        )

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

class TypeOfDeliverySchema(marshmallow.Schema):

    class Meta:
        fields = (
            'tipo_de_entrega',
            'costo_adicional'
        )

type_of_delivery_schema = TypeOfDeliverySchema()
types_of_delivery_schema = TypeOfDeliverySchema(many=True)