
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
from modules.v1.modelos.citas import Citas

AUTH_MICROSERVICE_URL = "http://" + os.getenv('AUTHENTICATION_HOST') + ":" + os.getenv('AUTHENTICATION_PORT') + "/auth/"
ADMIN_MICROSERVICE_URL = "http://" + os.getenv('ADMIN_HOST') + ":" + os.getenv('ADMIN_PORT') + "/admin"
ITEMS_POR_PAGINA = int(os.getenv('ITEMS_POR_PAGINA'))

# Creamos el Blueprint para el modulo de autenticacion
citas_v1_bp = Blueprint('citas_v1_bp', __name__)


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
            return jsonify({'msg': f'Acceso no autorizado'}), 403, {'Content-type' : 'application/json'}
        return wrapper
    return decorador_interno

DATETIME_STR_FORMAT = '%d/%m/%Y %H:%M:%S'

def str_2_datetime(fecha: str) -> datetime:
    # Convierte la fecha de string a datetime
    format = DATETIME_STR_FORMAT
    datetime_str = datetime.datetime.strptime(fecha, format)
    return datetime_str

def datetime_2_str(fecha: datetime) -> str:
    # Convierte la fecha de datetime a string
    format = DATETIME_STR_FORMAT
    #dateTime_str = time.strftime(format, fecha)
    dateTime_str = fecha.strftime(format)
    return dateTime_str

def check_datetime_format(fecha: str) -> bool:
    # Chequeamos que la fecha y hora estan en formato correcto.
    format = DATETIME_STR_FORMAT
    try:
        res = bool(datetime.datetime.strptime(fecha, format))
    except ValueError:
        res = False
    return res

@citas_v1_bp.route('/citas', methods = ['POST'])
@require_rol(['admin', 'paciente'])
def create_cita():

    """
        En BBDD se guarda:
            id_cita (PK)
            fecha
            motivo
            estado
            id_paciente (FK)
            id_doctor (FK)
            id_centro (FK)
            id_usuario_registra(FK)
    """
    # Obtenemos  el token
    auth_header = request.headers.get('Authorization')
    # Se usa para crear citas
    data = request.get_json()
    # Check que los parámetros esten bien infomrados.
    if data is None:
        return jsonify({'msg' : 'No hemos recibido los parámetros'}), 401, {'Content-type' : 'application/json'}
    if data.get('id_doctor') is None:
        return jsonify({'msg' : 'No hemos recibido el doctor'}), 401, {'Content-type' : 'application/json'}
    if data.get('id_centro') is None:
        return jsonify({'msg' : 'No hemos recibido el centro'}), 401, {'Content-type' : 'application/json'}
    if data.get('id_paciente') is None:
        return jsonify({'msg' : 'No hemos recibido el paciente'}), 401, {'Content-type' : 'application/json'}
    if data.get('fecha') is None or check_datetime_format(data.get('fecha')) == False:
        return jsonify({'msg' : 'No hemos recibido la fecha y hora en formato correcto DD/MM/YYYY HH:MM:SS'}), 401, {'Content-type' : 'application/json'}
    if data.get('motivo') is None:
        return jsonify({'msg' : 'No hemos recibido el motivo'}), 401, {'Content-type' : 'application/json'}
    
    """
        Validaciones
        El doctor existe.
        El centro médico existe.
        El paciente existe y está activo.
        No se puede agendar una cita si el doctor ya tiene otra en la misma fecha y
            hora (evitar doble reserva).
    """
    # Check si el doctor existe.
    dr_response = requests.get(url = f'{ADMIN_MICROSERVICE_URL}/doctores/{data["id_doctor"]}', headers= {'Authorization' : auth_header})
    if dr_response.status_code != 200:
        return dr_response.json(), dr_response.status_code, {'Content-type' : 'application/json'}
    # Check si el centro medico existe.
    centro_response = requests.get(url = f'{ADMIN_MICROSERVICE_URL}/centros/{data["id_centro"]}', headers={'Authorization' : auth_header})
    if centro_response.status_code != 200:
        return centro_response.json(), centro_response.status_code, {'Content-type' : 'application/json'}
    # Check si el paciente existe y está activo.
    paciente_response = requests.get(url = f'{ADMIN_MICROSERVICE_URL}/pacientes/{data["id_paciente"]}', headers = {'Authorization' : auth_header})
    if paciente_response.status_code != 200:
        return paciente_response.json(), paciente_response.status_code, {'Content-type' : 'application/json'}
    auth_response = requests.get(url= f'{AUTH_MICROSERVICE_URL}/id', headers={'Authorization' : auth_header})
    if auth_response.status_code != 200:
        return auth_response.json(), auth_response.status_code, {'Content-type' : 'application/json'}
    id_usuario = auth_response.json()['payload']['id']
    # Check si el doctor ya tiene una cita en la misma fecha y hora.
    cita = db.session.query(Citas).filter(Citas.id_doctor == data['id_doctor']).filter(Citas.fecha == str_2_datetime(data['fecha'])).first()
    if cita is not None:
        # Hay una cita pra ese doctor en esa fecha hora.
        return jsonify({'msg' : 'Ya existe otra cita para ese doctor en esa fecha'}), 401, {'Content-type' : 'application/json'}
    # Crea el objeto de la cita.
    cita = Citas(
        id_doctor = data['id_doctor'], 
        id_centro = data['id_centro'], 
        id_paciente = data['id_paciente'], 
        id_usuario_registra = id_usuario,
        fecha = str_2_datetime(data['fecha']), 
        motivo = data['motivo'], 
        estado = 'Activa'
        )
    db.session.add(cita)
    db.session.commit()
    return jsonify({'msg' : 'OK', 'payload' : cita.to_dict()}), 200, {'Content-type' : 'application/json'}

def _consulta_citas_as_admin(auth_hdr: str):
    # Implementa la logica de consulta como admin.
    # Admin: puede filtrar por doctor, centro, fecha, estado o paciente.
    # Se usan query params para aplicar los filtros.
    citas = db.session.query(Citas)
    dr = request.args.get('id_dr')
    if dr is not None:
        citas.filter(Citas.id_doctor == dr)
    centro = request.args.get('id_centro')
    if centro is not None:
        citas.filter(Citas.id_centro == centro)
    fecha = request.args.get('fecha')
    if fecha is not None:
        citas.filter(Citas.fecha == fecha)
    estado = request.args.get('estado')
    if estado is not None:
        citas.filter(Citas.estado == estado)
    paciente = request.args.get('id_paciente')
    if paciente is not None:
        citas.filter(Citas.id_paciente == paciente)
    citas = citas.all()
    json_citas = []
    for cita in citas:
        json_citas.append(cita.to_dict())
    return jsonify({'msg' : 'OK', 'payload' : json_citas}), 200, {'Content-type' : 'application/json'}



def _consulta_citas_as_secretario(auth_hdr: str):
    # Implementa la logica de consulta como secretario.
    # Secretaria: puede consultar citas filtrando por fecha.
    # Se usan query params para aplicar los filtros.
    
    fecha = rquest.args.get('fecha')
    if fecha is None:
        return jsonify({'msg' : 'No hemos recibido la fecha'}), 401, {'Content-type' : 'application/json'}
    citas = db.session.query(Citas).filter(Citas.fecha == fecha).all()
    json_citas = []
    for cita in citas:
        json_citas.append(cita.to_dict())
    return jsonify({'msg' : 'OK', 'payload' : json_citas}), 200, {'Content-type' : 'application/json'}

def _consulta_citas_as_doctor(auth_hdr: str):
    # Implementa la logica de consulta como doctor.
    # Doctor: solo ve sus propias citas.
    # Se usan query params para aplicar los filtros.
    
    # Primero obtengo el id del doctor que lo consulta (va en el token jwt)
    user_response = requests.get(url= f'{AUTH_MICROSERVICE_URL}/id', headers={'Authorization' : auth_hdr})
    if user_response != 200:
        return user_response.json(), user_response.status_code, {'Content-type' : 'application/json'}
    # Consulta el id del doctor segun el id_usuario.
    dr_response = requests.get(url=f'{ADMIN_MICROSERVICE_URL}/doctores/id', params= {'id_usr' : user_response.json()['payload']['id']})
    if dr_response.status_code != 200:
        return dr_response.json(), dr_response.status_code, {'Content-type' : 'application/json'}
    # Hacemos la select y ordenamos por fecha y que esten activas. para especificat que es de mas viejo a más antiguo,  hacemos un asc de  la columna
    citas = db.session.query(Citas).filter(Citas.id_doctor == dr_response.json()['payload']['id_doctor']).filter(Citas.estado == 'Activa').order_by(Citas.fecha.asc()).all()
    json_citas = []
    for cita in citas:
        json_citas.append(cita.to_dict())
    return jsonify({'msg' : 'OK', 'payload' : json_citas}), 200, {'Content-type' : 'application/json'}


@citas_v1_bp.route('/citas', methods = ['GET'])
@require_rol(['admin','doctor', 'secretario'])
def consulta_citas():
    # Se usa para listas las citas
    """
        Doctor: solo ve sus propias citas.
        Secretaria: puede consultar citas filtrando por fecha.
        Admin: puede filtrar por doctor, centro, fecha, estado o paciente.
        Se usan query params para aplicar los filtros.
    """
    # Obtenemos  el token
    auth_header = request.headers.get('Authorization')
    # Probamos los roles y segun el rol ejecutamos una u otra función.
    response = requests.get(url = f'{AUTH_MICROSERVICE_URL}/check', params = {'rol' : 'admin'} ,headers = {'Authorization' : auth_header})
    if response.status_code == 200:
        return _consulta_citas_as_admin(auth_hdr=auth_header)
    response = requests.get(url = f'{AUTH_MICROSERVICE_URL}/check', params = {'rol' : 'secretario'} ,headers = {'Authorization' : auth_header})
    if response.status_code == 200:
        return _consulta_citas_as_secretario(auth_hdr=auth_header)
    response = requests.get(url = f'{AUTH_MICROSERVICE_URL}/check', params = {'rol' : 'doctor'} ,headers = {'Authorization' : auth_header})
    if response.status_code == 200:
        return _consulta_citas_as_doctor(auth_hdr=auth_header)

@citas_v1_bp.route('/citas/<int:id>', methods = ['PUT'])
@require_rol(['admin','secretario'])
def cancela_cita(id:int):
    # Se usa para cambiar de estado la cita ( cancelarla )
    # Check si existe la cita.
    cita = db.session.query(Citas).filter(Citas.id_cita == id).first()
    if cita is None:
        return jsonify({'msg' : 'La cita a modificar NO existe'}), 404, { 'Content-type' : 'application/json'}
    cita.estado = 'Cancelada'
    # Forzamos la actualizacion  de los datos.
    db.session.flush()
    return jsonify({'msg' : 'OK', 'payload' : cita.to_dict()}), 200, {'Content-type' : 'application/json'}

# Debug.................................


# Endpoints para debug..................................................................................................................................
