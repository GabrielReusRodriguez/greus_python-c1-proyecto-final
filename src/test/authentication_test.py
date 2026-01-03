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
    response = requests.post(url = f'{URL}/login', json = {'user' : user, 'password' : password})
    return response.json()['token']

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
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'qwerty1'
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener el usuario creado"

def test_create_user_ko_existe_username():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'qwerty1'
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_create_user_ko_no_password():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'qwerty1'
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

    data = {}
    data['username'] = 'qwerty1'
    data['password'] = ''
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_create_user_ko_no_username():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_create_user_ko_no_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'qwerty2'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_create_user_ko_mal_rol():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'qwerty3'
    data['password'] = '1234567890'
    data['rol'] = 'ingeniero'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

    data = {}
    data['username'] = 'qwerty4'
    data['password'] = '1234567890'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

    data = {}
    data['username'] = 'qwerty5'
    data['password'] = '1234567890'
    data['rol'] = ''
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_create_user_ko_mal_metodo():
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'qwerty6'
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    response = requests.get(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_create_user_ko_no_login():
    data = {}
    data['username'] = 'qwerty7'
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    #response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    response = requests.post(url = f'{URL}/create_user', json = data)
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_create_user_ko_bad_login_rol():
    # Creo un usuario de pega
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'secretar'
    data['password'] = '1234567890'
    data['rol'] = 'secretario'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    # Login con el usuario que no tiene los roles.
    token = _login(user = 'secretar', password = '1234567890')
    data = {}
    data['username'] = 'qerty8'
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /auth/show_all    ***************************************************************************

def test_show_all_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/show_all', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len(response.json()['payload']) > 1, "Hay creados usuarios y nos devuelve la lista vacia."


def test_show_all_ko_mal_rol():
    # Creo un usuario de pega
    token = _login(user = 'admin', password = 'password')
    data = {}
    data['username'] = 'doctor'
    data['password'] = '1234567890'
    data['rol'] = 'medico'
    response = requests.post(url = f'{URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
    # Login con el usuario que no tiene los roles.
    token = _login(user = 'doctor', password = '1234567890')
    response = requests.get(url = f'{URL}/show_all', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_show_all_ko_no_login():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/show_all')
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_show_all_ko_mal_metodo():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/show_all', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"


# /auth/show/id    ***************************************************************************

def test_show_id_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/show/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta ha de contener el usuario"

def test_show_id_ko_no_login():
    response = requests.get(url = f'{URL}/show/1')
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

def test_show_id_ko_no_exists():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/show/100000', headers = {'Authorization' : f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"


def test_show_id_ko_mal_metodo():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/show/1', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"

# /auth/id         ****************************************************************************

def test_id_ok():
    token = _login(user = 'admin', password = 'password')
    response = requests.get(url = f'{URL}/id', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"
    assert response.json()['payload']['id'] == 1, "No se ha devuelto bien el id del usuario"

def test_id_ko_no_login():
    response = requests.get(url = f'{URL}/id')
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta ha de contener un mensaje"


def test_id_ko_mal_metodo():
    token = _login(user = 'admin', password = 'password')
    response = requests.post(url = f'{URL}/id', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
