from flask import Flask, request, jsonify, request
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

@application.route('/tiposUsuario/<tipo>')
def get_type_of_user(tipo):

    import schemas
    import models
    response = None

    try:
        type_of_user = models.TypeOfUsers.query.filter_by(nombre_del_tipo=tipo).first()
        
        if type_of_user:
            response = schemas.type_of_user_schema.dump(type_of_user)
        else:
            response = {"message": "No se ha encontrado ningún tipo de usuario"}
    except:
        response = {"message": "Ha ocurrido un problema"}

    return jsonify(response)

@application.route('/tiposUsuario/', methods=['POST'])
def regist_type_of_user():

    import models
    response = None

    try:
        name_of_type = request.json['tipo_de_usuario']
        new_type_of_user = models.TypeOfUsers(nombre_del_tipo=name_of_type)
        db.session.add(new_type_of_user)
        db.session.commit()

        response = {"message":"Tipo de usuario registrado con éxito"}
    except:
        response = {"message":"Ha ocurrido un problema al intentar registrar"}
    
    return jsonify(response)

@application.route('/tiposUsuario/<id>', methods=['PUT'])
def update_type_of_user(id):
    
    import models
    response = None

    try:
        type_of_user = db.session.query(models.TypeOfUsers).get(int(id))
        
        if type_of_user:
            type_of_user.nombre_del_tipo = request.json['tipo_de_usuario']
            response = {"message": "Tipo de usuario actualizado"}
            db.session.add(type_of_user)
            db.session.commit()
    
        else:
            response = {"message": "No se ha encontrado tipo de usuario"}
    except Exception as error:
        print(error)
        response = {"message": "Ha ocurrido un problema"}

    finally:
        return jsonify(response)
        
@application.route('/tiposUsuario/<id>', methods=['DELETE'])
def delete_type_of_user(id):
    
    import models 
    response = None
    
    try:
        type_of_user = db.session.query(models.TypeOfUsers).get(id)

        if type_of_user:
            
            db.session.delete(type_of_user)
            db.session.commit()

            response = {"message": "Tipo de usuario eliminado"}
        else:
            response = {"message": "No se ha encontrado tipo de usuario"}

    except:
        response = {"message": "Ha ocurrido un problema"}

    finally: 
        return jsonify(response)




@application.route('/usuarios/')
def get_users():

    import schemas
    import models

    all_users = models.Users.query.all()

    return jsonify(schemas.users_schema.dump(all_users))

@application.route('/usuarios/<dni>')
def get_user(dni):

    import models
    import schemas
    
    try:
        user = models.Users.query.filter_by(usuario_cedula_pkey=dni).first()
        if user:
            return jsonify(schemas.user_schema.dump(user))

        return jsonify({"message":"Usuario no encontrado"})
    
    except:
        return jsonify({"message": "Ha ocurrido un problema"})

@application.route('/usuarios/<dni>', methods=['PUT'])
def update_user(dni):

    import models
    import schemas

    response = None

    try:
        user = models.Users.query.filter_by(usuario_cedula_pkey=dni).first()
        if user:
            user.nombre = request.json['nombre']
            response = schemas.user_schema.dump(user)
            db.session.commit()
        
        else:
            response = {"Message": "No se ha encontrado ningun usuario"}
    except:
        response = {"Message": "Ha ocurrido un problema"}

    finally:
        return jsonify(response)

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

@application.route('/ingresos/<id>', methods=['PUT'])
def update_expense(id):

    import models 
    import schemas

    try:
        income = models.Incomes.query.filter_by(id_ingreso_pkey=id).first()
        if income:

            income.monto_ingreso = request.json['monto']
            db.session.commit()
            return jsonify(schemas.income_schema.dump(income))

        else:
            return jsonify({"message": "No se ha encontrado ingreso"})
    except Exception as error:
        print(error)
        return jsonify({"message":"Ha ocurrido un problema"})

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
