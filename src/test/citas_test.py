#!/bin/env python3

import pytest
import json
import requests

"""
    Clase de testing del microservice authentication
"""

SERVER = 'localhost'
PORT = 2205
URL = f'http://{SERVER}:{PORT}/citas'


def _login(user : str, password: str) -> str:
    response = requests.post(url = f'http://{SERVER}:2203/auth/login', json = {'user' : user, 'password' : password})
    return response.json()['token']

# /citas/citas/ POST
def test_citasPOST_ok():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_1'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_1'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_1'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    print(f'Respuesta CITA: {response.status_code} msg :{response.json()}')
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"

    """
    if data.get('id_doctor') is None:
        return jsonify({'msg' : 'No hemos recibido el doctor'}), 401, {'Content-type' : 'application/json'}
    if data.get('id_centro') is None:
        return jsonify({'msg' : 'No hemos recibido el centro'}), 401, {'Content-type' : 'application/json'}
    if data.get('id_paciente') is None:
        return jsonify({'msg' : 'No hemos recibido el paciente'}), 401, {'Content-type' : 'application/json'}
    if data.get('fecha') is None:
        return jsonify({'msg' : 'No hemos recibido la fecha y hora'}), 401, {'Content-type' : 'application/json'}
    if data.get('motivo') is None:
        return jsonify({'msg' : 'No hemos recibido el motivo'}), 401, {'Content-type' : 'application/json'}
    """
"""
def test_citasPOST_ko_bad_rol():
    pass
"""

def test_citasPOST_ko_no_login():
    
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_3'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_3'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_3'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {})
    print(f'Respuesta CITA: {response.status_code} msg :{response.json()}')
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_citasPOST_ko_bad_method():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_4'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_4'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_4'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.get(url = f'{URL}/citas', json = data, headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
"""

def test_citasPOST_ko_no_data():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_5'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_5'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_5'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    response = requests.post(url = f'{URL}/citas', json = {}, headers = {'Authorization': f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_citasPOST_ko_mal_rol():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_100'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_100'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_100'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    token = _login(user= 'citas_dr_100' , password = '1234567890')
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    print(f'Respuesta CITA: {response.status_code} msg :{response.json()}')
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_citasPOST_ko_no_fecha():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_7'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_7'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_7'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    #data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    print(f'Respuesta CITA: {response.status_code} msg :{response.json()}')
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


def test_citasPOST_ko_no_motivo():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_8'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_8'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_8'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    #data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    print(f'Respuesta CITA: {response.status_code} msg :{response.json()}')
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


"""
def test_citasPOST_ko_no_estado():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_9'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_9'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_9'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    print(f'Respuesta CITA: {response.status_code} msg :{response.json()}')
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
"""

def test_citasPOST_ko_existe():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_9'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_9'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_9'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    code = 401
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"


# /citas/citas GET 

def test_citasGET_ko_bad_rol():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_200'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_200'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_200'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/2025 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/2025 16:01:00'
    data['motivo'] = 'Dolor de muelas 2'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user = 'citas_paciente_200' , password='1234567890')
    response = requests.get(url = f'{URL}/citas', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_citasGET_ko_no_login():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_201'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_201'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_201'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/2025 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/2025 16:01:00'
    data['motivo'] = 'Dolor de muelas 2'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.get(url = f'{URL}/citas', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_citasGET_ko_bad_method():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_202'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_202'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_202'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '20/02/2025 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/2025 11:01:00'
    data['motivo'] = 'Dolor de muelas 2'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.post(url = f'{URL}/citas', headers = {'Authorization' : f'Bearer {token}'})
    code = 405
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    #assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
"""


def test_citasGET_ok_doctor():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_1000'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_1000'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_1000'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '23/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.get(url = f'{URL}/citas', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']), "La respuesta ha de contener más de una cita"


def test_citasGET_ok_admin():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_9000'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_9000'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_9000'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1983 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '23/02/1983 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    
    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '23/02/1983 11:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    
    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '23/02/1983 12:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    
    requests.put(url = f'{URL}/citas/{response.json()['payload']['id_cita']}', headers  = {'Authorization' :f'Bearer {token}'})

    # Las busquedas
    response = requests.get(url = f'{URL}/citas',params = {'fecha' : '23/02/1983'}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener más de una cita"

    response = requests.get(url = f'{URL}/citas',params = {'fecha' : '23/02/2026'}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) == 0, "La respuesta ha de contener más de una cita"

    response = requests.get(url = f'{URL}/citas',params = {'estado' : 'Activa'}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener más de una cita"


    #response = requests.get(url = f'{URL}/citas',params = {}, headers = {'Authorization' : f'Bearer {token}'})
    #assert 1 == 0 , f"JSON: {response.json()}"

    response = requests.get(url = f'{URL}/citas',params = {'estado' : 'Cancelada'}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) == 1, f"La respuesta ha de contener más de una cita {response.json()}"

    response = requests.get(url = f'{URL}/citas',params = {'centro' : response_centros.json()['payload']['id_centro']}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener más de una cita"

    response = requests.get(url = f'{URL}/citas',params = {'id_paciente' : response_paciente.json()['payload']['id_paciente']}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener más de una cita"

    response = requests.get(url = f'{URL}/citas',params = {'id_dr' : response_doctor.json()['payload']['id_doctor']}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener más de una cita"


def test_citasGET_ok_secretario():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_2000'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_2000'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_2000'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el secretario
    data = {}
    data = {}
    data['rol'] = 'secretario'
    data['username'] = 'citas_secretario_2000'
    data['password'] = '1234567890'
    response = requests.post(url = f'http://{SERVER}:2204/admin/usuarios', json = data, headers = {'Authorization': f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1983 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '23/02/1983 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '23/02/1983 11:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user= 'citas_secretario_2000', password = '1234567890')
    response = requests.get(url = f'{URL}/citas',params = {'fecha' : '23/02/1983'}, headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"
    assert len (response.json()['payload']) > 1, "La respuesta ha de contener más de una cita"
    


# /citas/<ID> PUT

def test_citasIDPut_ok():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_400'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_400'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_400'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.put(url = f'{URL}/citas/{response.json()['payload']['id_cita']}', headers = {'Authorization' : f'Bearer {token}'})
    code = 200
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
    assert 'payload' in response.json(), "La respuesta  ha de contener un payload"


def test_citasIDPut_ko_bad_rol():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_500'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_500'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_500'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    token = _login(user =  'citas_dr_500', password= '1234567890')
    response = requests.put(url = f'{URL}/citas/{response.json()['payload']['id_cita']}', headers = {'Authorization' : f'Bearer {token}'})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

def test_citasIDPut_ko_no_login():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_700'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_700'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_700'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.put(url = f'{URL}/citas/{response.json()['payload']['id_cita']}', headers = {})
    code = 403
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"

"""
def test_citasIDPut_ko_bad_method():
    pass
"""

def test_citasIDPut_ko_no_exists():
    token = _login(user= 'admin' , password='password')
    data = {}
    # Creo el doctor
    data['rol'] = 'doctor'
    data['username'] = 'citas_dr_600'
    data['password'] = '1234567890'
    data['nombre']  = 'Gabriel Reus'
    data['especialidad'] = 'ondontologia'
    response_doctor = requests.post(url = f'http://{SERVER}:2204/admin/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})
    print(f'Respuesta doctor: {response_doctor.status_code} msg :{response_doctor.json()}')
    
    # Creo el paciente
    data = {}
    data['rol'] = 'paciente'
    data['username'] = 'citas_paciente_600'
    data['password'] = '1234567890'
    data['telefono'] = '912312312'
    data['nombre'] = 'GRR'
    data['estado'] = 'Activo'
    response_paciente = requests.post(url = f'http://{SERVER}:2204/admin/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Creo el centro
    data = {}
    data['direccion'] = 'Barcelona'
    data['nombre'] = 'citas_centro_600'
    response_centros = requests.post(url = f'http://{SERVER}:2204/admin/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    data = {}
    data['id_doctor'] = response_doctor.json()['payload']['id_doctor']
    data['id_centro'] = response_centros.json()['payload']['id_centro']
    data['id_paciente'] = response_paciente.json()['payload']['id_paciente']
    data['fecha'] = '22/02/1982 14:01:00'
    data['motivo'] = 'Dolor de muelas'
    response = requests.post(url = f'{URL}/citas', json = data, headers = {'Authorization': f'Bearer {token}'})
    response = requests.put(url = f'{URL}/citas/50000', headers = {'Authorization' : f'Bearer {token}'})
    code = 404
    assert response.status_code == code, f"El codigo de estado debe ser {code}"
    assert 'msg' in response.json(), "La respuesta  ha de contener un mensaje"
