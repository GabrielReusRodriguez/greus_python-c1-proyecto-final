
"""

Script del microservicio responsable de crear los tokens JWT.

"""

from flask import Blueprint, jsonify
import jwt

# Creamos el Blueprint para el modulo de autenticacion
auth_v1_bp = Blueprint('auth_v1_bp', __name__)

@auth_v1_bp.route('/', methods=['GET'])
def helloWorld():
    return jsonify({'mensaje': 'OK'})
