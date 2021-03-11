from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config_files.database_flask_config import configDatabase

application = Flask(__name__)
configDatabase(application)

marshmallow = Marshmallow(application)
db = SQLAlchemy(application)

@application.route('/tiposUsuario/')
def get_type_of_users():

    import schemas
    import models

    all_type_of_users = models.TypeOfUsers.query.all()
    schema_type_of_users = schemas.type_of_users_schema.dump(all_type_of_users)

    return jsonify(schema_type_of_users)

@application.route('/usuarios/')
def get_users():

    import schemas
    import models

    all_users = models.Users.query.all()
    schema_all_users = schemas.users_schema.dump(all_users)

    return jsonify(schema_all_users)

@application.route('/usuarios/<dni>')
def get_user(dni):

    import models
    import schemas
    
    try:
        user = models.Users.query.filter_by(usuario_cedula_pkey=dni).first()
        
        if user:
            user_schema = schemas.user_schema.dump(user)
            return jsonify(user_schema)

        return jsonify({"message":"Usuario no encontrado"})
    
    except Exception as error:
        print(error)
        return jsonify({"message": "Ha ocurrido un problema"})
        
@application.route('/direcciones/')
def get_directions():

    import schemas
    import models

    all_directions = models.Directions.query.all()
    schema_all_directions = schemas.directions_schema.dump(all_directions)

    return jsonify(schema_all_directions)

@application.route('/egresos/')
def get_expenses():

    import schemas
    import models

    all_expenses = models.Expenses.query.all()
    schema_all_expenses = schemas.expenses_schema.dump(all_expenses)

    return jsonify(schema_all_expenses)

@application.route('/ingresos/')
def get_incomes():

    import schemas
    import models

    all_incomes = models.Incomes.query.all()
    schema_all_incomes = schemas.incomes_schema.dump(all_incomes)

    return jsonify(schema_all_incomes)

@application.route('/clientes/')
def get_clients():

    import schemas
    import models

    all_clients = models.Clients.query.all()
    schema_all_clients = schemas.clients_schema.dump(all_clients)

    return jsonify(schema_all_clients)

@application.route('/pedidos/')
def get_orders():

    import schemas
    import models

    all_orders = models.Orders.query.all()
    schema_all_orders = schemas.orders_schema.dump(all_orders)

    return jsonify(schema_all_orders)

@application.route('/productos/')
def all_products():

    import schemas
    import models

    all_products = models.Products.query.all()
    schema_all_products = schemas.products_schema.dump(all_products)

    return jsonify(schema_all_products)

@application.route('/tiposEntrega/')
def all_types_of_delivery():

    import schemas
    import models

    all_types_of_delivery = models.TypesOfDelivery.query.all()
    schema_all_types_of_delivery = schemas.types_of_delivery_schema.dump(all_types_of_delivery)
    
    return jsonify(schema_all_types_of_delivery)

if __name__ == '__main__':
    application.run(debug=True)
