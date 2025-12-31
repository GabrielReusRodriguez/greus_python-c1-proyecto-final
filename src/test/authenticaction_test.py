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

# /auth/show_all    ***************************************************************************

# /auth/show/id    ***************************************************************************

# /auth/id         ****************************************************************************

