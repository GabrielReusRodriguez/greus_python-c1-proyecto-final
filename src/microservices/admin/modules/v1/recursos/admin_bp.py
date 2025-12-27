
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
    token = auth_header.split(" ")[1]
    # Obtenemos los parámetros json.
    data = request.get_json()
    # Check... solo checqueo el rol ya que el resto se comprobará en el microservicio de autenticacion.
    if data is None:
        return jsonify({'msg' : 'No hemos recibodo parámetros'}), 401, {'Content-type' : 'application/json'}
    if data.get('rol') is None or data.get('rol') not in ('admin', 'secretario'):
        return jsonify({'msg' : 'No hemos recibido el rol'}), 401, {'Content-type' : 'application/json'}
    response = requests.post(url=AUTH_MICROSERVICE_URL + "create_user", json = data, headers= {'Authorization' : f"Bearer {token}"})
    if response.status_code != 200:
        return response.json(), response.status_code, {'Content-type' : 'application/json'}
    # Si ha llegado hasta aqui, significa que el usuario se ha creado bien por lo que seguimos creando el tipo de usuario = medico, admin...
    return response.json, 200, {'Content-type' : 'application/json'}

@admin_v1_bp.route('/usuarios?<int:pagina>', methods=['GET'])
@require_rol(['admin', 'secretario'])
def consulta_usuarios(pagina:int):
    # Este endpoint consulta usuarios de tipo secretario y admin.
    #requests.get(url=AUTH_MICROSERVICE_URL + "show_all")
    pass

@admin_v1_bp.route('/usuario?<int:id>', methods=['GET'])
def consulta_usuario(id:int):
    pass

@admin_v1_bp.route('/doctores', methods=['POST'])
@require_rol('admin')
def create_doctor():
    pass

@admin_v1_bp.route('/pacientes', methods=['POST'])
@require_rol('admin')
def create_paciente():
    pass


@admin_v1_bp.route('/pacientes?<int:pagina>', methods=['GET'])
def consulta_pacientes(pagina : int):
    # Recuerda paginacion!!!
    pass

@admin_v1_bp.route('/paciente?<int:id>', methods=['GET'])
def consulta_paciente(id : int):
    pass


@admin_v1_bp.route('/centros',methods=['POST'])
@require_rol('admin')
def create_centro():
    pass


@admin_v1_bp.route('/centros?<int:pagina>', methods=['GET'])
def consulta_centros(pagina : int):
    # Recuerda paginacion!!!
    pass

@admin_v1_bp.route('/centro?<int:id>', methods=['GET'])
def consulta_centro(id : int):
    pass



#Busqueda completa.

# Endpoints para debug..................................................................................................................................
