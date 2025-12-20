
"""

Script del microservicio responsable de crear los tokens JWT.

"""

from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt

# Creamos el Blueprint para el modulo de autenticacion
auth_v1_bp = Blueprint('auth_v1_bp', __name__)

# El endpoint para hacer login, esto genera el token si se autentica bien.
@auth_v1_bp.route('/login', methods=['GET'])
def login():
    # Obtenemos las credenciales de acceso que nos envia el usuario.
    credenciales = request.get_json()
    if credenciales is None:
        return jsonify({'mensaje': 'No hemos recibido las credenciales'}), 401, {'Content-type' : 'application/json'}

    return jsonify({'mensaje': 'OK'})
