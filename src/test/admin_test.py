#!/bin/env python3

import pytest
import json
import requests

"""
    Clase de testing del microservice authentication
"""

SERVER = 'localhost'
PORT = 2203
URL = f'http://{SERVER}:{PORT}/auth'


def _login(user : str, password: str) -> str:
    response = requests.post(url = f'{URL}/login', json = {'user' : 'admin', 'password' : 'password'})
    return response.json()['token']

# /admin/usuario

def test_usuario_ok():
    pass

def test_usuario_ko_bad_rol():
    pass

def test_usuario_ko_no_login():
    pass

def test_usuario_ko_bad_method():
    pass

def test_usuario_ko_no_data():
    pass

def test_usuario_ko_no_rol():
    pass

# /admin/usuarios

def test_usuarios_ok():
    pass

def test_usuarios_ko_bad_rol():
    pass

def test_usuarios_ko_no_login():
    pass

def test_usuario_ko_bad_method():
    pass

def test_usuario_ko_exists():
    pass

# /admin/usuarios/id
def test_usuariosId_ok():
    pass

def test_usuariosId_ko_bad_rol():
    pass

def test_usuariosId_ko_no_login():
    pass

def test_usuarioId_ko_bad_method():
    pass

def test_usuarioId_ko_noexists():
    pass

# /admin/doctores POST
def test_doctoresPOST_ok():
    pass

def test_doctoresPOST_ko_bad_rol():
    pass

def test_doctoresPOST_ko_no_login():
    pass

def test_doctoresPOST_ko_bad_method():
    pass

def test_doctoresPOST_ko_no_data():
    pass

def test_doctoresPOST_ko_bad_rol():
    pass

def test_doctoresPOST_ko_no_nombre():
    pass

def test_doctoresPOST_ko_no_especialidad():
    pass

def test_doctoresPOST_ko_existe():
    pass

# /admin/doctores GET

def test_doctoresGET_ok():
    pass

def test_doctoresGET_ko_bad_rol():
    pass

def test_doctoresGET_ko_no_login():
    pass

def test_doctoresGET_ko_bad_method():
    pass

# /admin/doctores/<id>
def test_doctoresID_ok():
    pass

def test_doctoresID_ko_bad_rol():
    pass

def test_doctoresID_ko_no_login():
    pass

def test_doctoresID_ko_bad_method():
    pass

def test_doctoresID_ko_no_exists():
    pass

# /admin/doctores/id
def test_doctoresIDUser_ok():
    pass

def test_doctoresIDUser_ko_bad_rol():
    pass

def test_doctoresIDUser_ko_no_login():
    pass

def test_doctoresIDUser_ko_bad_method():
    pass

def test_doctoresIDUser_ko_no_exists():
    pass

# /admin/pacientes POST
def test_pacientesPOST_ok():
    pass

def test_pacientesPOST_ko_bad_rol():
    pass

def test_pacientesPOST_ko_no_login():
    pass

def test_pacientesPOST_ko_bad_method():
    pass

def test_pacientesPOST_ko_no_data():
    pass

def test_pacientesPOST_ko_bad_rol():
    pass

def test_pacientesPOST_ko_no_telf():
    pass

def test_pacientesPOST_ko_no_nombre():
    pass

def test_pacientesPOST_ko_no_estado():
    pass

def test_pacientesPOST_ko_existe():
    pass


# /admin/pacientes GET

def test_pacientesGET_ok():
    pass

def test_pacientesGET_ko_bad_rol():
    pass

def test_pacientesGET_ko_no_login():
    pass

def test_pacientesGET_ko_bad_method():
    pass

# /admin/pacientes/<id>
def test_pacientesID_ok():
    pass

def test_pacientesID_ko_bad_rol():
    pass

def test_pacientesID_ko_no_login():
    pass

def test_pacientesID_ko_bad_method():
    pass

def test_pacientesID_ko_no_exists():
    pass

# /admin/pacientes/id

def test_pacientesIDUser_ok():
    pass

def test_pacientesIDUser_ko_bad_rol():
    pass

def test_pacientesIDUser_ko_no_login():
    pass

def test_pacientesIDUser_ko_bad_method():
    pass

def test_pacientesIDUser_ko_no_exists():
    pass

# /admin/centros POST
def test_centrosPOST_ok():
    pass

def test_centrosPOST_ko_bad_rol():
    pass

def test_centrosPOST_ko_no_login():
    pass

def test_centrosPOST_ko_bad_method():
    pass

def test_centrosPOST_ko_no_data():
    pass

def test_centrosPOST_ko_bad_rol():
    pass

def test_centrosPOST_ko_no_direccion():
    pass

def test_centrosPOST_ko_no_nombre():
    pass

def test_centrosPOST_ko_existe():
    pass


# /admin/centros GET
def test_centrosGET_ok():
    pass

def test_centrosGET_ko_bad_rol():
    pass

def test_centrosGET_ko_no_login():
    pass

def test_centrosGET_ko_bad_method():
    pass


# /admin/centros/<id>

def test_centrosID_ok():
    pass

def test_centrosID_ko_bad_rol():
    pass

def test_centrosID_ko_no_login():
    pass

def test_centrosID_ko_bad_method():
    pass

def test_centrosID_ko_no_exists():
    pass


"""
# /auth/login service *********************************************************************
def test_login_ok():
    response = requests.post(url = f'{URL}/login', json = {'user' : 'admin', 'password' : 'password'})
    assert response.status_code == 200, "El codigo de estado debe ser 200"
    assert response.json() is not None, 'La respuesta debe ser json'
    assert 'token' in response.json(), 'La respuesta debe contener un token.'

def test_login_ko_password():
    response = requests.post(url = f'{URL}/login', json = {'user' : 'admin', 'password' : 'password2'})
    assert response.status_code == 403, "El codigo de estado debe ser 403"
    assert response.json() is not None, 'La respuesta debe ser json'
    assert 'msg' in response.json(), 'El mensaje debe estar en el token'

def test_login_ko_username():
    response = requests.post(url = f'{URL}/login', json = {'user' : 'admin2', 'password' : 'password'})
    assert response.status_code == 403, "El codigo de estado debe ser 403"
    assert response.json() is not None, 'La respuesta debe ser json'
    assert 'msg' in response.json(), 'El mensaje debe estar en el token'

def test_login_no_user():
    response = requests.post(url = f'{URL}/login', json = {'password' : 'password'})
    assert response.status_code == 401, "El codigo de estado debe ser 401"
    assert response.json() is not None, 'La respuesta debe ser json'
    assert 'msg' in response.json(), 'El mensaje debe estar en el token'

def test_login_no_password():
    response = requests.post(url = f'{URL}/login', json = {'user' : 'admin'})
    assert response.status_code == 401, "El codigo de estado debe ser 401"
    assert response.json() is not None, 'La respuesta debe ser json'
    assert 'msg' in response.json(), 'El mensaje debe estar en el token'

def test_login_no_payload():
    response = requests.post(url = f'{URL}/login')
    code = 415
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_login_wrong_method():
    response = requests.get(url = f'{URL}/login')
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"


# /auth/check service *********************************************************************

def test_check_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/check?rol=admin', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert response.json()['msg'] == 'OK', "El msg ha de ser OK"

def test_check_no_login():
    response = requests.get(url = f'{URL}/check?rol=admin')
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"

def test_check_bad_rol():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/check?rol=secretario', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"

def test_check_no_rol():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/check', headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"

# /auth/create_user ***************************************************************************
def test_create_user_ok():
    pass

def test_create_user_ko_existe_username():
    pass

def test_create_user_ko_no_password():
    pass

def test_create_user_ko_no_username():
    pass

def test_create_user_ko_no_rol():
    pass

def test_create_user_ko_mal_rol():
    pass

def test_create_user_ko_mal_metodo():
    pass

def test_create_user_ko_no_login():
    pass

# /auth/show_all    ***************************************************************************

def test_show_all_ok():
    pass

def test_show_all_ko_mal_rol():
    pass

def test_show_all_ko_no_login():
    pass

def test_show_all_ko_mal_metodo():
    pass

# /auth/show/id    ***************************************************************************

def test_show_id_ok():
    pass

def test_show_id_ko_no_login():
    pass

def test_show_id_ko_mal_metodo():
    pass

# /auth/id         ****************************************************************************

def test_id_ok():
    pass

def test_id_ko_no_login():
    pass

def test_id_ko_mal_metodo():
    pass

"""