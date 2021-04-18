from flask import Flask, request, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import simplejson

from config_files.database_flask_config import configDatabase

application = Flask(__name__)
configDatabase(application)

marshmallow = Marshmallow(application)
db = SQLAlchemy(application)

#tipos de usuario

@application.route('/tiposUsuario/')
def get_type_of_users():

    import schemas
    import models

    all_type_of_users = db.session.query(models.TypeOfUsers).all()
    schema_type_of_users = schemas.type_of_users_schema.dump(all_type_of_users)

    return jsonify(schema_type_of_users)

@application.route('/tiposUsuario/<tipo>')
def get_type_of_user(tipo):

    import schemas
    import models
    
    response = None

    try:
        type_of_user = db.session.query(models.TypeOfUsers)\
        .filter_by(nombre_del_tipo=tipo).first()
        
        if type_of_user:
            response = schemas.type_of_user_schema.dump(type_of_user)
        else:
            response = {
            "message": "No se ha encontrado ningún tipo de usuario"
        }
    except:
        response = {"message": "Ha ocurrido un problema"}

    return jsonify(response)

@application.route('/tiposUsuario/', methods=['POST'])
def create_type_of_user():

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
    except:
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
        
#usuarios
        
@application.route('/usuarios/')
def get_users():

    import schemas
    import models

    response = None
    
    try:
        all_users = db.session.query(models.Users, models.TypeOfUsers)\
        .join(
            models.Users, 
            models.Users.tipo_de_usuario_foreign==models.TypeOfUsers.tipo_de_usuario_pkey
        )
    
        if all_users:
            users_dict = {}
            counter = 0

            for user in all_users:
        
                counter += 1
                users_dict['user {}'.format(counter)] = schemas.users_schema.dump(user)
        
            response = users_dict
        else:
            response = {
                "message": "No existen usuarios"
            }
    except:
        response = {
            "message": "Ha ocurrido un problema"
        }
    finally:
        return jsonify(response)

@application.route('/usuarios/<dni>')
def get_user(dni):

    import models
    import schemas

    response = None

    try:

        search_user = db.session.query(models.Users, models.TypeOfUsers)\
        .filter_by(usuario_cedula_pkey=dni)\
        .join(
            models.Users, 
            models.Users.tipo_de_usuario_foreign==models.TypeOfUsers.tipo_de_usuario_pkey
        ).first()

        if search_user:
            response = schemas.users_schema.dump(search_user)
        else:
            response = {
                "message": "No se ha encontrado el usuario"
            }
    except:
        response = {
            "message": "Ha ocurrido un problema"
        }

    finally:
        return jsonify(response)

@application.route('/usuarios/', methods=['POST'])
def create_user():

    import models
    response = None

    try:
        
        data_new_user = {
            "usuario_cedula_pkey": request.json['cedula'],
            "nombre": request.json['nombre'],
            "apellido_paterno": request.json['apellido_paterno'],
            "apellido_materno": request.json['apellido_materno'],
            "correo": request.json['correo'],
            "telefono": request.json['telefono'],
            "contraseña": request.json['contrasena'],
            "estado": int(request.json['estado']),
            "tipo_de_usuario_foreign": int(request.json['tipo_de_usuario'])
        }
        
        new_user = models.Users(**data_new_user)

        db.session.add(new_user)
        db.session.commit()

        response = {"message": "Usuario creado"}
    except Exception as error:
        print(error)
        response = {"message": "Ha ocurrido un problema"}

    finally:
        return jsonify(response)

@application.route('/usuarios/<dni>', methods=['PUT'])
def update_user(dni):

    import models
    import schemas

    response = None

    try:
        user = db.session.query(models.Users).get(dni)
        if user:
            
            user.nombre = request.json['nombre']
            user.apellido_paterno = request.json['apellido_paterno']
            user.apellido_materno = request.json['apellido_materno']
            user.correo = request.json['correo']
            user.telefono = request.json['telefono']
            user.contraseña = request.json['contrasena']
            user.estado = int(request.json['estado'])

            db.session.add(user)
            db.session.commit()

            response = {
                "message": "Usuario actualizado"
            }
        else:
            response = {
                "message": "No se ha encontrado ningun usuario"
            }
    except:
        response = {
            "message": "Ha ocurrido un problema"
        }
    finally:
        return jsonify(response)

@application.route('/usuarios/<dni>', methods=['DELETE'])
def delete_user(dni):

    import models
    response = None

    try:
        user = db.session.query(models.Users).get(dni)
        if user:

            db.session.delete(user)
            db.session.commit()

            response = {
                "message": "Usuario eliminado"
            }
        else:
            response = {
                "message": "Usuario no encontrado"
            }
    except: 
        response = {
            "message": "Ha ocurrido un problema"
        }
            
    finally:
        return jsonify(response)

#direcciones 

@application.route('/direcciones/')
def get_directions():

    import schemas
    import models
    response = None

    try:
        all_directions = models.Directions.query.all()
        
        if all_directions:
            response = schemas.directions_schema.dump(all_directions)
        else:
            response = {"message": "No hay direcciones"}
    except:
        response = {"message": "Ha ocurrido un problema"}
    finally:
        return jsonify(response)

@application.route('/direcciones/<id>')
def get_direction(id):

    import schemas 
    import models
    response = None

    try:
        direction = db.session.query(models.Directions).get(id)

        if direction:
            schema_direction = schemas.direction_schema.dump(direction)
            response = schema_direction
        else:
            response = {"message": "No se ha encontrado direccion"}
    except: 
        response = {"message": "Ha ocurrido un problema"}

    finally:
        return jsonify(response)

@application.route('/direcciones/', methods=['POST'])
def create_direction():
    
    import models
    
    response = None
    
    try:
        data_direction = {
            "ciudad": request.json['ciudad'],
            "barrio": request.json['barrio'],
            "direccion": request.json['direccion']
        }
  
        new_direction = models.Directions(**data_direction)
        
        db.session.add(new_direction)
        db.session.commit()
        
        response = {
            "message": "Direccion registrada"
        }
        
    except Exception as error:
        print(error)
        response = {
            "message": "Ha ocurrido un problema en el registro"
        }
    finally:
        return jsonify(response)
    
@application.route('/direcciones/<id>', methods=['PUT'])
def update_direction(id): 
    
    import models
    response = None
    
    direction_data = {
        "ciudad": request.json['ciudad'],
        "barrio": request.json['barrio'],
        "direccion": request.json['direccion']
    }
    
    try:
        direction = db.session.query(models.Directions).get(id)
        
        if direction:
            
            direction.ciudad = direction_data['ciudad']
            direction.barrio = direction_data['barrio']
            direction.direccion = direction_data['direccion']
            
            db.session.add(direction)
            db.session.commit()
            
            response = {
                "message": "direccion actualizada"
            }
        else:
            response = {
                "message": "No se ha encontrado direccion"
            }
    except Exception as error:
        
        print(error)
       
        response = {
            "message": "Ha ocurrido un problema"
        }
        
    finally:
        return jsonify(response)
        
# egresos
    
@application.route('/egresos/')
def get_expenses():
    
    import models
    import schemas
    
    response = None
    
    try:
        expenses = db.session.query(models.Expenses).all()
    
        if expenses:
            
            expenses_schema = schemas.expenses_schema.dump(expenses)
            
            for expense in expenses_schema:
                expense['peso'] = round(expense['peso'], 2)
            
            response = expense
            
        else:
            response = {
                "message": "No hay egresos"
            }
    except:
        response = {
            "message": "Ha ocurrido un problema"
        }
        
    finally:
        return jsonify(response)

@application.route('/egresos/', methods=['POST'])
def create_expense():
    
    import models
    response = None
    
    data_expense = {
        "fecha_egreso": request.json['fecha_egreso'],
        "material": request.json['material'],
        "cantidad": request.json['cantidad'],
        "proveedor": request.json['proveedor'],
        "costo": request.json['costo'],
        "peso": request.json['peso']
    }
    
    try:
        new_expense = models.Expenses(**data_expense)
        db.session.add(new_expense)
        db.session.commit()
        
        response = {
            "message": "Se ha registrado el ingreso"
        }
        
    except:
        response = {
            "message": "Ha ocurrido un problema"
        }
        
    finally:
        return jsonify(response)

@application.route('/egresos/<id>', methods=['PUT'])
def update_expense(id):
    
    import models
    import schemas
    
    response = None
    
    try:
        
        egreso = db.session.query(models.Expenses).get(id)
        
        if egreso:
            
            data_expense_update = {
                "fecha_egreso": request.json['fecha_egreso'],
                "material": request.json['material'],
                "cantidad": request.json['cantidad'],
                "proveedor": request.json['proveedor'],
                "costo": request.json['costo'],
                "peso": request.json['peso']
            } 
        
            egreso.fecha_egreso = data_expense_update['fecha_egreso']
            egreso.material = data_expense_update['material']
            egreso.cantidad = data_expense_update['cantidad']
            egreso.proveedor = data_expense_update['proveedor']
            egreso.costo = data_expense_update['costo']
            egreso.peso = data_expense_update['peso']
        
            db.session.add(egreso)
            db.session.commit()
        
            response = {
                "message": "Datos actualizados"
            }
            
        else:
            response = {
                "message": "No se ha encontrado egreso"
            }
    except:
    
        response = {
            "message": "Ha ocurrido un problema"
        }
        
    finally:
        return jsonify(response)

@application.route('/egresos/<id>', methods=['DELETE'])
def delete_expense(id):
    
    import models
    response = None
    
    try:
        egreso = db.session.query(models.Expenses).get(id)
        
        if egreso:
            
            db.session.delete(egreso)
            db.session.commit()
            
            response = {
                "message": "Egreso eliminado"
            }
            
        else:
            response = {
                "message": "Egreso no encontrado"
            }
    except:
            response = {
                "message": "Egreso eliminado"
            }
    finally:
        return response

# clientes

@application.route('/clientes/', methods=['POST'])
def create_client():
    
    import models 
    import schemas
    
    response = None
    
    data_client = {
        "nombre": request.json['nombre'],
        "apellido": request.json['apellido'],
        "telefono": request.json['telefono'],
        "direccion_id_foreign": request.json['direccion_id']
    }
    
    try:
        
        new_client = models.Clients(**data_client)
        db.session.add(new_client)
        db.session.commit()
        
        response = {
            "message": "Cliente creado correctamente"
        }
    
    except:
        
        response = {
            "message": "Ha ocurrido un problema"
        }
    
    finally:
        
        return jsonify(response)
        
@application.route('/clientes/<id>')
def get_clients(id):

    import schemas
    import models
    
    response = None

    try:
        client = db.session.query(models.Clients, models.Directions)\
        .filter_by(cliente_id_pkey=id)\
        .join(
            models.Clients,
            models.Clients.direccion_id_foreign==models.Directions.direccion_id_pkey
        ).first()

        if client:
            
            response = schemas.clients_schema.dump(client)

        else:
            response = {
                "message": "No hay clientes registrados"
            }
        
    except Exception as error:
        print(error)
        response = {
            "message": "Ha ocurrido un problema"
        }
    
    finally:
        return jsonify(response)

@application.route('/clientes/<id>', methods=['PUT'])
def update_client(id):

    import models   
    import schemas

    response = None

    try:
        data_update = {
            "nombre": request.json['nombre'],
            "apellido": request.json['apellido'],
            "telefono": request.json['telefono']
        }

        client = db.session.query(models.Clients).get(id)
        
        if client:
            client.nombre = data_update['nombre']
            client.apellido = data_update['apellido']
            client.telefono = data_update['telefono']
            db.session.add(client)
            db.session.commit()

            response = {
                "message": "Cliente actualizado"
            }
            
        else:
            response = {
                "message": "Cliente no encontrado"
            }

    except Exception as error:
        print(error)
        response = {
            "message": "Ha ocurrido un problema"
        }

    finally:
        return jsonify(response)

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
