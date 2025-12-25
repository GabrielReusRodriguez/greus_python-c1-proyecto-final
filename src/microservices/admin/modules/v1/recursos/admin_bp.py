
"""

Script del microservicio responsable de crear  y gestionar  cenrtos, pacientes yt doctores.

"""

from flask import Blueprint, jsonify, request
import datetime
from functools import wraps

from db import db

#import modules.v1.modelos.usuario
from modules.v1.modelos.paciente import Paciente
from modules.v1.modelos.doctor import Doctor
from modules.v1.modelos.centro import CentroMedico



# Creamos el Blueprint para el modulo de autenticacion
admin_v1_bp = Blueprint('admin_v1_bp', __name__)


#Defino el decorador con parámetro require_rol para checkear los roles cuando llamamos a la funcion
def require_rol(rol_requerido):
    def decorador_interno(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            pass
            """
            global JWT_SECRET
            # 1. Validación del token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'msg': 'No hemos recibido el jwt'}), 401, {'Content-type' : 'application/json'}
            # Hago un split del contenido de authentication y pillo la segunda palñabra ya que es Authorization: Bearer <token>
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(jwt = token, key = JWT_SECRET, verify= True, algorithms =['HS256'])
                usuario = payload['sub']
                # Busco el usuario para ver si existe y recupero su rol.
                user = db.session.query(Usuario).filter(Usuario.username == usuario).first()
                if user is None:
                    return jsonify({'msg' : 'JWT Token inválido'}), 403, {'Content-type' : 'application/json'}
                 # 2. Verificación del permiso
                rol_del_usuario = user.rol
                if rol_del_usuario != rol_requerido:
                    return jsonify({'msg': 'Permiso denegado'}), 403, {'Content-type' : 'application/json'}
                return f(*args, **kwargs)
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError,jwt.InvalidSignatureError):
                return jsonify({'msg': 'JWT Token invalido'}), 401, {'Content-type' : 'application/json'}
            """
        return wrapper
    return decorador_interno


#print(f"1. SECRET: {JWT_SECRET} SESSION_TIME {JWT_SESSION_TIME}")

# El endpoint para crea un usuario con rol admin o secretaria.
@admin_v1_bp.route('/usuario', methods=['POST'])
def create_usuario():
    pass
    """
    # Declaramos la variables del env como globales.
    global JWT_SECRET
    global JWT_SESSION_TIME

    # Obtenemos las credenciales de acceso que nos envia el usuario.
    credenciales = request.get_json()
    if credenciales is None:
        return jsonify({'msg': 'No hemos recibido las credenciales'}), 401, {'Content-type' : 'application/json'}
    
    # Primero checkeamos el usuario y pass
    if credenciales.get('user') is None:
        return jsonify({'msg': 'No hemos recibido el user'}), 401, {'Content-type' : 'application/json'}
    if credenciales.get('password') is None:
        return jsonify({'msg': 'No hemos recibido el password'}), 401, {'Content-type' : 'application/json'}
    
    #usuario = Usuario.query().filter(Usuario.username == credenciales['user']).filter(Usuario.password == credenciales['password']).first()
    usuario = db.session.query(Usuario).filter(Usuario.username == credenciales['user']).filter(Usuario.password == credenciales['password']).first()
    if usuario is None:
        return jsonify({'msg': 'Login fallado'}), 404, {'Content-type' : 'application/json'}

    # Generamos el token si hemos encotnrado el usuario y password
    payload = {
        'sub' : credenciales['user'],
        'iat' : datetime.datetime.utcnow(),
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = JWT_SESSION_TIME)
    }
    token = jwt.encode(payload = payload, key = JWT_SECRET)
    return jsonify({'token' : token}), 200, {'Content-type' : 'application/json'}

@auth_v1_bp.route('/check', methods=['GET'])
def check():
    # Checkea que el token JWT es valido. He decidido hacerlo con GET ya que le pasaré el token en el header Authoritation y devolveré un json en caso OK. con el rol.
    global JWT_SECRET

    # Obtengo el rol que quiero comprobar. de los parámetros de query.
    rol = request.args.get('rol')
    if rol is None:
        return jsonify({'msg': 'No hemos el rol a comprobar'}), 401, {'Content-type' : 'application/json'}        

    # Obtengo el token JWT a validar
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'msg': 'No hemos recibido el jwt'}), 401, {'Content-type' : 'application/json'}
    # Hago un split del contenido de authentication y pillo la segunda palñabra ya que es Authorization: Bearer <token>
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(jwt = token, key = JWT_SECRET, verify= True, algorithms =['HS256'])
        usuario = payload['sub']
        # Busco el usuario para ver si existe y recupero su rol.
        user = db.session.query(Usuario).filter(Usuario.username == usuario).first()
        if user is None:
            return jsonify({'msg' : 'JWT token inválido'}), 403, {'Content-type' : 'application/json'}
        if user.rol == rol:
            # Hemos encontrado el usuario,  y tiene el rol adecuado.
            return jsonify({'msg' : 'OK'}), 200, {'Content-type' : 'application/json'}
        else:
            # Tenemos user pero no es del rol que nos piden.
            return jsonify({'msg' : 'No autorizado.'}), 403, {'Content-type' : 'application/json'}
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError,jwt.InvalidSignatureError):
        return jsonify({'msg': 'Token invalido'}), 401, {'Content-type' : 'application/json'}
    """

@admin_v1_bp.route('/usuarios?<int:pagina>', methods=['GET'])
def consulta_usuarios(pagina:int):
    pass

@admin_v1_bp.route('/usuario?<int:id>', methods=['GET'])
def consulta_usuario(id:int):
    pass

@admin_v1_bp.route('/doctores', methods=['POST'])
@require_rol('admin')
def create_doctor():
    pass
    """
    # Con este método, creamos un usuario y lo metemos en la base de datos.
    payload = request.get_json()
    # Check de argumetnos.
    if payload is None or payload.get('username') is None or payload.get('password') is None or payload.get('rol') is None:
        return jsonify({'msg' : 'No hemos recibido los datos necesarios del usuario'}), 401, {'Content-type' : 'application/json'}
    # Check del username
    if len(payload['username']) < 4:
        return jsonify({'msg': 'El username es demasiado corto'}), 401, {'Content-type' : 'application/json'}
    if db.session.query(Usuario).filter(Usuario.username == payload['username']).first() is not None:
        return jsonify({'msg': 'El username ya está utilizado'}), 401, {'Content-type' : 'application/json'}
    # Check del password
    if len(payload['password']) < 4:
        return jsonify({'msg': 'El password es demasiado corto'}), 401, {'Content-type' : 'application/json'}
    # Check del rol => NO se puede crear otro admin.
    if payload['rol'] not in ('medico', 'secretario', 'paciente'):
        return jsonify({'msg': 'El rol no es correcto'}), 401, {'Content-type' : 'application/json'}
    # Creamos la instancia del usuario
    user = Usuario(username= payload['username'], password = payload['password'], rol = payload['rol'])
    # agregamos la instancia a la BBDD
    db.session.add(user)
    # Hacemos commit
    db.session.commit()
    return jsonify(user.to_dict()), 200, {'Content-type' : 'application/json'}
    """

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
