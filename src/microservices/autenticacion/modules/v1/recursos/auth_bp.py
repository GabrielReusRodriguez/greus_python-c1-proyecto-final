
"""

Script del microservicio responsable de crear los tokens JWT.

"""

from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt
from db import db

#import modules.v1.modelos.usuario
from modules.v1.modelos.usuario import Usuario


# Creamos el Blueprint para el modulo de autenticacion
auth_v1_bp = Blueprint('auth_v1_bp', __name__)

# El endpoint para hacer login, esto genera el token si se autentica bien.
@auth_v1_bp.route('/login', methods=['GET'])
def login():
    # Obtenemos las credenciales de acceso que nos envia el usuario.
    #credenciales = request.get_json()
    #if credenciales is None:
    #    return jsonify({'mensaje': 'No hemos recibido las credenciales'}), 401, {'Content-type' : 'application/json'}

    return jsonify({'mensaje': 'OK'}), 200, {'Content-type' : 'application/json'}

@auth_v1_bp.route('/create_user', methods=['GET'])
def create_user():
    # Con este método, creamos un usuario y lo metemos en la base de datos.
    user = Usuario(username= 'a', password = 'b', rol = 'c')
    db.session.add(user)
    db.session.commit()
    return jsonify({'mensaje': 'OK'}), 200, {'Content-type' : 'application/json'}



@auth_v1_bp.route('/show_all', methods = ['GET'])
def show_all():
    # Con este metodo enseño todos los usuarios que hay
    session = db.session
    results = session.query(Usuario).all()
    usuarios = []
    for user in results:
       usuarios.append(user.to_dict())
    return jsonify({'mensaje': 'OK', 'payload' : usuarios}), 200, {'Content-type' : 'application/json'}


