#!/bin/env python3

import pytest
import json
import requests

"""
    Clase de testing del microservice authentication
"""

SERVER = 'localhost'
PORT = 2204
URL = f'http://{SERVER}:{PORT}/admin'


def _login(user : str, password: str) -> str:
    response = requests.post(url = f'http://{SERVER}:2203/auth/login', json = {'user' : user, 'password' : password})
    if response.status_code != 200:
        print(f"status code{response.status_code} token: {response.json()}")
    return response.json()['token']
    

# /admin/usuarios POST

def test_usuario_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'poiuyt0'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta debe contener el usuario creado"

def test_usuario_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'poiuyt0adfccszddca'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'poiuyt0qw12fsrd'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"    

def test_usuario_ko_no_login():
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'poiuyt0'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data)
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_usuario_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'poiuyt0'
    data['password'] = '1234567890'
    #response = requests.get(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.get(url = f'{URL}/usuarios', headers = {'Authorization': f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_usuario_ko_no_data():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/usuarios', headers = {'Authorization': f'Bearer {token}'})
    code = 415
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_usuario_ko_no_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = ''
    data['username'] = 'poiuyt02'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

    data = {}
    data['username'] = 'poiuyt03'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_usuario_ko_exists():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'admin'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

# /admin/usuarios GET

def test_usuarios_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/usuarios', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los usuarios"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener mas de un usuario"


def test_usuarios_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'asdwqegtdsgbed'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    response = requests.get(url = f'{URL}/usuarios', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_usuarios_ko_no_login():
    response = requests.get(url = f'{URL}/usuarios')
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_usuario_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/usuarios', json = {},headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

# /admin/usuarios/id
def test_usuariosId_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/usuarios/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"
        
def test_usuariosId_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = '1asdwqegtdsgbed'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    response = requests.get(url = f'{URL}/usuarios/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_usuariosId_ko_no_login():
    response = requests.get(url = f'{URL}/usuarios/1', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_usuariosId_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/usuarios/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"


def test_usuariosId_ko_noexists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/usuarios/1000', headers = {'Authorization' : f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /admin/doctores POST
def test_doctoresPOST_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '2asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"


def test_doctoresPOST_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = '3asdwqegtdsgbed'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '3asdwqegtdsgbed3'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresPOST_ko_no_login():
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '4asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_doctoresPOST_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '02asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.get(url = f'{URL}/doctores',  headers={'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
"""

def test_doctoresPOST_ko_no_data():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/doctores', json = {},  headers={'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresPOST_ko_error_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'admin'
    data['username'] = '12asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresPOST_ko_no_nombre():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '32asdwqegtdsgbed'
    data['password'] = '1234567890'
    #data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresPOST_ko_no_especialidad():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '2asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    #data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresPOST_ko_existe():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '2asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

# /admin/doctores GET

def test_doctoresGET_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/doctores', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"

def test_doctoresGET_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'secretario'
    data['username'] = '113asegtdsgbed'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    response = requests.get(url = f'{URL}/doctores', headers = {'Authorization': f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresGET_ko_no_login():
    response = requests.get(url = f'{URL}/doctores', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_doctoresGET_ko_bad_method():
    pass
"""

# /admin/doctores/<id>
def test_doctoresID_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '22asdwqegtdsgbed'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus 2'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    response = requests.get(url = f'{URL}/doctores/1', headers={'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"

def test_doctoresID_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '22asdwqegtdsgbed23434'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus 2'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    response = requests.get(url = f'{URL}/doctores/1', headers={'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresID_ko_no_login():
    response = requests.get(url = f'{URL}/doctores/1', headers={})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresID_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/doctores/1', json = {}, headers={'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"


def test_doctoresID_ko_no_exists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/doctores/4568', headers={'Authorization' : f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /admin/doctores/id
def test_doctoresIDUser_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'doctor'
    data['username'] = '001asddas'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus 2'
    data['especialidad'] = 'ondontologia'
    response = requests.post(url = f'{URL}/doctores', json = data,  headers={'Authorization' : f'Bearer {token}'})
    response = requests.get(url = f'{URL}/doctores/id', params = {'id_usr' : response.json()['payload']['id_usuario']}, headers = {'Authorization': f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"

def test_doctoresIDUser_ko_bad_rol():
    token = _login(user = '22asdwqegtdsgbed', password = '1234567890')
    response = requests.get(url = f'{URL}/doctores/id', params = {'id_usr' : 1}, headers = {'Authorization': f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresIDUser_ko_no_login():
    response = requests.get(url = f'{URL}/doctores/id', params = {'id_usr' : 1}, headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_doctoresIDUser_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/doctores/id', params = {'id_usr' : 1}, headers = {'Authorization': f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_doctoresIDUser_ko_no_exists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/doctores/id', params = {'id_usr' : 1000}, headers = {'Authorization': f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /admin/pacientes POST
def test_pacientesPOST_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"

def test_pacientesPOST_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_2'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    token = _login(user = data['username'], password = data['password'])
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesPOST_ko_no_login():
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_3'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_pacientesPOST_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_4'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.get(url = f'{URL}/pacientes', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
"""

def test_pacientesPOST_ko_no_data():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_5'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', headers = {'Authorization' : f'Bearer {token}'})
    code = 415
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    #assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesPOST_ko_no_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    #data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_6'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesPOST_ko_no_telf():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_7'
    data['password'] = '1234567890'
    #data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesPOST_ko_no_nombre():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_8'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    #data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesPOST_ko_no_estado():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897_9'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    #data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesPOST_ko_existe():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'sdasdasdasdasds897897'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /admin/pacientes GET

def test_pacientesGET_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/pacientes', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"
    assert len(response.json()['payload']) > 1, "La repsuesta ha de devolver pacientes"

def test_pacientesGET_ko_bad_rol():
    token = _login(user = 'sdasdasdasdasds897897', password = '1234567890')
    response = requests.get(url = f'{URL}/pacientes', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesGET_ko_no_login():
    response = requests.get(url = f'{URL}/pacientes', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_pacientesGET_ko_bad_method():
    pass
"""

# /admin/pacientes/<id>
def test_pacientesID_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'paciente01'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data,  headers={'Authorization' : f'Bearer {token}'})
    response = requests.get(url = f'{URL}/pacientes/{response.json()['payload']['id_paciente']}', headers = {'Authorization': f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"


def test_pacientesID_ko_bad_rol():
    token = _login(user = 'paciente01', password = '1234567890')
    response = requests.get(url = f'{URL}/pacientes/1', headers = {'Authorization': f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_pacientesID_ko_no_login():
    response = requests.get(url = f'{URL}/pacientes/1', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_pacientesID_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/pacientes/1', headers = {'Authorization': f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_pacientesID_ko_no_exists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/pacientes/1000', headers = {'Authorization': f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /admin/pacientes/id

def test_pacientesIDUser_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'paciente02'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data,  headers={'Authorization' : f'Bearer {token}'})
    response = requests.get(url = f'{URL}/pacientes/id', params = {'id_usr': response.json()['payload']['id_usuario']}, headers = {'Authorization': f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"


def test_pacientesIDUser_ko_bad_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'paciente03'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data,  headers={'Authorization' : f'Bearer {token}'})
    token = _login(user = data['username'], password= data['password'])
    response = requests.get(url = f'{URL}/pacientes/id', params = {'id_usr': response.json()['payload']['id_usuario']}, headers = {'Authorization': f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_pacientesIDUser_ko_no_login():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'paciente04'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response = requests.post(url = f'{URL}/pacientes', json = data,  headers={'Authorization' : f'Bearer {token}'})
    response = requests.get(url = f'{URL}/pacientes/id', params = {'id_usr': response.json()['payload']['id_usuario']}, headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_pacientesIDUser_ko_bad_method():
    pass
"""

def test_pacientesIDUser_ko_no_exists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/pacientes/id', params = {'id_usr': 10000}, headers = {'Authorization': f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

# /admin/centros POST
def test_centrosPOST_ok():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['nombre'] = 'centro1'
    data['direccion'] = 'direccion'
    response = requests.post(url = f'{URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'} )
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"

def test_centrosPOST_ko_bad_rol():
    token = _login(user = 'paciente02', password = '1234567890')
    data = {}
    data['nombre'] = 'centro1'
    data['direccion'] = 'direccion'
    response = requests.post(url = f'{URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'} )
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_centrosPOST_ko_no_login():
    data = {}
    data['nombre'] = 'centro1'
    data['direccion'] = 'direccion'
    response = requests.post(url = f'{URL}/centros', json = data, headers = {} )
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_centrosPOST_ko_bad_method():
    pass
"""

def test_centrosPOST_ko_no_data():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/centros', json = {}, headers = {'Authorization' : f'Bearer {token}'} )
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_centrosPOST_ko_no_direccion():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['nombre'] = 'centro1'
    #data['direccion'] = 'direccion'
    response = requests.post(url = f'{URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'} )
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_centrosPOST_ko_no_nombre():
    token = _login(user = 'admin', password = 'password')
    data = {}
    #data['nombre'] = 'centro1'
    data['direccion'] = 'direccion'
    response = requests.post(url = f'{URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'} )
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_centrosPOST_ko_existe():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['nombre'] = 'centro1'
    data['direccion'] = 'direccion'
    response = requests.post(url = f'{URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'} )
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /admin/centros GET
def test_centrosGET_ok():
    token = _login(user = 'admin', password = 'password')
    response= requests.get(url = f'{URL}/centros', headers= {'Authorization': f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"
    assert len(response.json()) > 1, "La respuesta ha de contener más de un centro"


def test_centrosGET_ko_bad_rol():
    token = _login(user = 'paciente01', password = '1234567890')
    response= requests.get(url = f'{URL}/centros', headers= {'Authorization': f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_centrosGET_ko_no_login():
    response= requests.get(url = f'{URL}/centros', headers= {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


"""
def test_centrosGET_ko_bad_method():
    pass
"""

# /admin/centros/<id>

def test_centrosID_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/centros/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener los datos de usuario"


def test_centrosID_ko_bad_rol():
    token = _login(user = 'paciente02', password = '1234567890')
    response = requests.get(url = f'{URL}/centros/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_centrosID_ko_no_login():
    response = requests.get(url = f'{URL}/centros/1', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"



def test_centrosID_ko_bad_method():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/centros/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_centrosID_ko_no_exists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/centros/100', headers = {'Authorization' : f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


