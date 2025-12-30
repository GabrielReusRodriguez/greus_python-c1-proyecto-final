
"""

Script del microservicio responsable de crear  y gestionar  cenrtos, pacientes yt doctores.

"""

from flask import Blueprint, jsonify, request
import datetime
import requests
import os
from functools import wraps

from db import db

#import modules.v1.modelos.usuario
from modules.v1.modelos.paciente import Paciente
from modules.v1.modelos.doctor import Doctor
from modules.v1.modelos.centro import CentroMedico


AUTH_MICROSERVICE_URL = "http://" + os.getenv('AUTHENTICATION_HOST') + ":" + os.getenv('AUTHENTICATION_PORT') + "/auth/"
ITEMS_POR_PAGINA = int(os.getenv('ITEMS_POR_PAGINA'))

# Creamos el Blueprint para el modulo de autenticacion
admin_v1_bp = Blueprint('admin_v1_bp', __name__)


#Defino el decorador con parámetro require_rol para checkear los roles cuando llamamos a la funcion
def require_rol(roles_requeridos : list):
    def decorador_interno(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Para comprobarlo, llamaremos al endpoint de authentication para checkear el rol.
            # Obtengo el token JWT a validar
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return jsonify({'msg': 'No hemos recibido el jwt', 'head' : auth_header}), 403, {'Content-type' : 'application/json'}
            # Hago un split del contenido de authentication y pillo la segunda palñabra ya que es Authorization: Bearer <token>
            token = auth_header.split(" ")[1]
            for rol in roles_requeridos:
                resp = requests.get(url = AUTH_MICROSERVICE_URL + "check", params= {'rol' : rol}, headers= {'Authorization' : f"Bearer {token}"})
                if resp.status_code == 200:
                    return f(*args, **kwargs)        
            return jsonify({'msg': 'Acceso no autorizado'}), 403, {'Content-type' : 'application/json'}
        return wrapper
    return decorador_interno


# El endpoint para crea un usuario con rol admin o secretaria.
@admin_v1_bp.route('/usuario', methods=['POST'])
@require_rol(['admin'])
def create_usuario():
    # Obtengo el token jwt
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify({'msg': 'No hemos recibido el jwt'}), 403, {'Content-type' : 'application/json'}
    # Hago un split del contenido de authentication y pillo la segunda palñabra ya que es Authorization: Bearer <token>
    #token = auth_header.split(" ")[1]
    # Obtenemos los parámetros json.
    data = request.get_json()
    # Check... solo checqueo el rol ya que el resto se comprobará en el microservicio de autenticacion.
    if data is None:
        return jsonify({'msg' : 'No hemos recibodo parámetros'}), 401, {'Content-type' : 'application/json'}
    if data.get('rol') is None or data.get('rol') not in ('admin', 'secretario'):
        return jsonify({'msg' : 'No hemos recibido el rol'}), 401, {'Content-type' : 'application/json'}
    response = requests.post(url=AUTH_MICROSERVICE_URL + "create_user", json = data, headers= {'Authorization' : auth_header})
    if response.status_code != 200:
        return response.json(), response.status_code, {'Content-type' : 'application/json'}
    # Si ha llegado hasta aqui, significa que el usuario se ha creado bien por lo que seguimos creando el tipo de usuario = medico, admin...
    return response.json(), 200, {'Content-type' : 'application/json'}

@admin_v1_bp.route('/usuarios', methods=['GET'])
@require_rol(['admin'])
def consulta_usuarios():
    # Nos devuelve un listado de n usuarios de rol admin y secretario
    # Obtengo el token jwt
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify({'msg': 'No hemos recibido el jwt'}), 403, {'Content-type' : 'application/json'}
    pagina = request.args.get('pagina')
    if pagina is None:
        pagina = 0 
    # Este endpoint consulta usuarios de tipo secretario y admin.
    response = requests.get(url=AUTH_MICROSERVICE_URL + "show_all", headers ={'Authorization' : auth_header})
    if response.status_code != 200:
        return response.json(), response.status_code, {'Content-type' : 'application/json'}
    data = response.json()
    i = 0
    inicio_pagina = ITEMS_POR_PAGINA * pagina
    users = []
    #Itero usuario por usuario buscando roles admin y secretario.
    for user in data['payload']:
        if user['rol'] == 'admin' or user['rol'] == 'secretario':
            if i >= inicio_pagina:
                # Borro el password ( por seguridad)
                user['password'] = ''
                users.append(user)
            i = i + 1
        if len(users) > ITEMS_POR_PAGINA:
            break
    return jsonify({'msg' : 'OK', 'payload' : users}), 200, {'Content-type' : 'application/json'}

@admin_v1_bp.route('/usuarios/<int:id>', methods=['GET'])
@require_rol(['admin'])
def consulta_usuario(id:int):
    # Este endpoint consulta el usuario de tipo secretario y admin que le pasamos por parámetro 
    # Obtengo el token jwt
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify({'msg': 'No hemos recibido el jwt'}), 403, {'Content-type' : 'application/json'}
    response = requests.get(url = AUTH_MICROSERVICE_URL + f"show/{id}", headers={'Authorization' : header})
    return response.json(), response.status_code, {'Content-type' : 'application/json'}
    

@admin_v1_bp.route('/doctores', methods=['POST'])
@require_rol(['admin'])
def create_doctor():
    # Obtengo el token jwt
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify({'msg': 'No hemos recibido el jwt'}), 403, {'Content-type' : 'application/json'}
    # Obtenemos los parámetros json.
    data = request.get_json()
    # Check... solo checqueo el rol ya que el resto se comprobará en el microservicio de autenticacion.
    if data is None:
        return jsonify({'msg' : 'No hemos recibodo parámetros'}), 401, {'Content-type' : 'application/json'}
    if data.get('rol') is None or data.get('rol') not in ('doctor'):
        return jsonify({'msg' : 'No hemos recibido el rol correcto'}), 401, {'Content-type' : 'application/json'}
    if data.get('nombre') is None:
        return jsonify({'msg': 'No hemos recibido el nombre'}), 401, {'Content-type' : 'application/json'}
    if data.get('especialidad') is None:
        return jsonify({'msg': 'No hemos recibido la especialidad'}), 401, {'Content-type' : 'application/json'}
    response = requests.post(url=AUTH_MICROSERVICE_URL + "create_user", json = data, headers= {'Authorization' : auth_header})
    if response.status_code != 200:
        return response.json(), response.status_code, {'Content-type' : 'application/json'}
    # Tenemos el user creado, ahopra creamos los datos del doctor.
    dr = Doctor(nombre= data.get('nombre'), especialidad = data.get('especialidad'), id_usuario = response.json()['payload']['id_usuario'])
    db.session.add(dr)
    db.session.commit()
    # Si ha llegado hasta aqui, significa que el usuario se ha creado bien por lo que seguimos creando el tipo de usuario = medico, admin...
    return jsonify({'msg' : 'OK', 'payload' : dr.to_dict()}), 200, {'Content-type' : 'application/json'}

@admin_v1_bp.route('/doctores', methods=['GET'])
@require_rol(['admin'])
def consulta_doctores():
    # Devuelvo la lista de doctores
    doctores = []
    pagina = request.args.get('pagina')
    if pagina is None:
        pagina = 0 
    i = 0
    inicio_pagina = ITEMS_POR_PAGINA * pagina
    # Select de los drs.
    results = db.session.query(Doctor).all()
    for result in results:
        if i >= inicio_pagina:
            # creo el json del dr.
            doctores.append(result.to_dict())
        if len(doctores) > ITEMS_POR_PAGINA:
            break
        i = i + 1
    return jsonify({'msg' : 'OK', 'payload' : doctores}), 200, {'Content-type' : 'application/json'}

    """
    i = 0
    inicio_pagina = ITEMS_POR_PAGINA * pagina
    users = []
    #Itero usuario por usuario buscando roles admin y secretario.
    for user in data['payload']:
        if user['rol'] == 'admin' or user['rol'] == 'secretario':
            if i >= inicio_pagina:
                # Borro el password ( por seguridad)
                user['password'] = ''
                users.append(user)
            i = i + 1
        if len(users) > ITEMS_POR_PAGINA:
            break
    return jsonify({'msg' : 'OK', 'payload' : users}), 200, {'Content-type' : 'application/json'}
    """

@admin_v1_bp.route('/doctores/<int:id>', methods=['GET'])
@require_rol(['admin'])
def consulta_doctor(id : int):
    # Devuelvo el Doctor por id de doctor.
    dr = db.session.query(Doctor).filter(Doctor.id_doctor == id).first()
    if dr is None:
        return jsonify({'msg' : 'OK'}), 404, {'Content-type' : 'application/json'}
    return jsonify({'msg' : 'OK' , 'payload' : dr.to_dict()}), 200, {'Content-type' : 'application/json'}


@admin_v1_bp.route('/pacientes', methods=['POST'])
@require_rol(['admin'])
def create_paciente():
    """
        Paciente
        Datos mínimos del paciente:

        id_paciente (PK)
        id_usuario (FK opcional)
        nombre
        teléfono
        estado(ACTIVO/INACTIVO)
    """
    # Obtengo el token jwt
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify({'msg': 'No hemos recibido el jwt'}), 403, {'Content-type' : 'application/json'}
    # Obtenemos los parámetros json.
    data = request.get_json()
    # Check... solo checqueo el rol ya que el resto se comprobará en el microservicio de autenticacion.
    if data is None:
        return jsonify({'msg' : 'No hemos recibido parámetros'}), 401, {'Content-type' : 'application/json'}
    if data.get('telefono') is None:
        return jsonify({'msg' : 'No hemos recibido el teléfono'}), 401, {'Content-type' : 'application/json'}
    if data.get('nombre') is None:
        return jsonify({'msg': 'No hemos recibido el nombre'}), 401, {'Content-type' : 'application/json'}
    if data.get('estado') is None:
        return jsonify({'msg': 'No hemos recibido el estado'}), 401, {'Content-type' : 'application/json'}
    response = requests.post(url=AUTH_MICROSERVICE_URL + "create_user", json = data, headers= {'Authorization' : auth_header})
    if response.status_code != 200:
        return response.json(), response.status_code, {'Content-type' : 'application/json'}
    # Tenemos el user creado, ahopra creamos los datos del doctor.
    paciente = Paciente(nombre= data.get('nombre'), teléfono= data.get('telefono'),estado = data.get('estado'), id_usuario  = response.json()['payload']['id_usuario'])
    db.session.add(paciente)
    db.session.commit()
    # Si ha llegado hasta aqui, significa que el usuario se ha creado bien por lo que seguimos creando el tipo de usuario = medico, admin...
    return jsonify({'msg' : 'OK', 'payload' : paciente.to_dict()}), 200, {'Content-type' : 'application/json'}


@admin_v1_bp.route('/pacientes?<int:pagina>', methods=['GET'])
@require_rol(['admin'])
def consulta_pacientes(pagina : int):
    # Recuerda paginacion!!!
    pacientes = []
    pagina = request.args.get('pagina')
    if pagina is None:
        pagina = 0 
    i = 0
    inicio_pagina = ITEMS_POR_PAGINA * pagina
    results = db.session.query(Paciente).all()
    for result in results:
        if i >= inicio_pagina:
            # Añado el paciente
            pacientes.append(result.to_dict())
        if len(pacientes) > ITEMS_POR_PAGINA:
            break
        i = i + 1
    return jsonify({'msg' : 'OK', 'payload' : pacientes}), 200, {'Content-type' : 'application/json'}

@admin_v1_bp.route('/pacientes/<int:id>', methods=['GET'])
@require_rol(['admin'])
def consulta_paciente(id : int):
    # Obtenemos un paciente.
    paciente = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
    if paciente is None:
        return jsonify({'msg': 'OK'}),404,{'Content-type' : 'application/json'}
    return jsonify({'msg' : 'OK' , 'payload' : paciente.to_dict()}), 200, {'Content-type': 'application/json'}


@admin_v1_bp.route('/centros',methods=['POST'])
@require_rol(['admin'])
def create_centro():
    """
    Centro Médico
        id_centro (PK)
        nombre
        direccion
    """
    # Creo un centro.
    # Obtenemos los parámetros json.
    data = request.get_json()
    # Check... solo checqueo el rol ya que el resto se comprobará en el microservicio de autenticacion.
    if data is None:
        return jsonify({'msg' : 'No hemos recibido parámetros'}), 401, {'Content-type' : 'application/json'}
    if data.get('direccion') is None:
        return jsonify({'msg' : 'No hemos recibido la direccion'}), 401, {'Content-type' : 'application/json'}
    if data.get('nombre') is None:
        return jsonify({'msg': 'No hemos recibido el nombre'}), 401, {'Content-type' : 'application/json'}

    # Creamos el centro...
    centro = CentroMedico(nombre= data.get('nombre'), direccion = data.get('direccion'))
    db.session.add(centro)
    db.session.commit()
    # Si ha llegado hasta aqui, significa que el usuario se ha creado bien por lo que seguimos creando el tipo de usuario = medico, admin...
    return jsonify({'msg' : 'OK', 'payload' : centro.to_dict()}), 200, {'Content-type' : 'application/json'}
    


@admin_v1_bp.route('/centros?<int:pagina>', methods=['GET'])
def consulta_centros(pagina : int):
    centros = []
    pagina = request.args.get('pagina')
    if pagina is None:
        pagina = 0 
    i = 0
    inicio_pagina = ITEMS_POR_PAGINA * pagina
    results = db.session.query(CentroMedico).all()
    for result in results:
        if i >= inicio_pagina:
            # Añado el paciente
            centros.append(result.to_dict())
        if len(centros) > ITEMS_POR_PAGINA:
            break
        i = i + 1
    return jsonify({'msg' : 'OK', 'payload' : centros}), 200, {'Content-type' : 'application/json'}


@admin_v1_bp.route('/centros/<int:id>', methods=['GET'])
def consulta_centro(id : int):
    # Obtenemos un paciente.
    centro = db.session.query(CentroMedico).filter(CentroMedico.id_centro == id).first()
    if centro is None:
        return jsonify({'msg': 'OK'}),404,{'Content-type' : 'application/json'}
    return jsonify({'msg' : 'OK' , 'payload' : centro.to_dict()}), 200, {'Content-type': 'application/json'}

#Busqueda completa.

# Endpoints para debug..................................................................................................................................
