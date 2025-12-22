
"""

Script del microservicio responsable de crear los tokens JWT.

"""

from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from db import db
from env_manager import *

#import modules.v1.modelos.usuario
from modules.v1.modelos.usuario import Usuario

# Creamos el Blueprint para el modulo de autenticacion
auth_v1_bp = Blueprint('auth_v1_bp', __name__)


#print(f"1. SECRET: {JWT_SECRET} SESSION_TIME {JWT_SESSION_TIME}")

# El endpoint para hacer login, esto genera el token si se autentica bien.
@auth_v1_bp.route('/login', methods=['POST'])
def login():
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

    # Obtengo el token JWT a validar
    """
    params = request.get_json()
    if params is None or params.get('token') is None:
        return jsonify({'msg': 'No hemos recibido el token JWT'}), 401, {'Content-type' : 'application/json'}
    """
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
        # Hemos encontrado el usuario, devuelvo el rol correspondiente.
        return jsonify({'msg' : 'OK', 'rol' : user.rol}), 200, {'Content-type' : 'application/json'}
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({'msg': 'Token invalido'}), 401, {'Content-type' : 'application/json'}



# Endpoints para debug..................................................................................................................................
@auth_v1_bp.route('/create_user', methods=['GET'])
def create_user():
    # Con este método, creamos un usuario y lo metemos en la base de datos.
    user = Usuario(username= 'a', password = 'b', rol = 'c')
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'OK'}), 200, {'Content-type' : 'application/json'}


@auth_v1_bp.route('/show_all', methods = ['GET'])
def show_all():
    # Con este metodo enseño todos los usuarios que hay
    session = db.session
    results = session.query(Usuario).all()
    usuarios = []
    for user in results:
       usuarios.append(user.to_dict())
    return jsonify({'msg': 'OK', 'payload' : usuarios}), 200, {'Content-type' : 'application/json'}

@auth_v1_bp.route('/show/<int:id>', methods = ['GET'])
def show(id):
    # Nos muestra los datos de un único usuario.
    return jsonify({'msg': 'OK'}), 200, {'Content-type' : 'application/json'}

"""
@auth_v1_bp.route('/check', methods=['POST'])
def check():
    # Validamos el token jwt.
    return jsonify({'msg': 'OK'}), 200, {'Content-type' : 'application/json'}
"""