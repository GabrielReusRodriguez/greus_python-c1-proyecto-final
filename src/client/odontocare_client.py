#!/bin/env python3

"""
Script que cumple los requisitos del enunciado:
Cliente Python
    El estudiante debe entregar un script: carga_inicial.py, que:
    1. Realice login con un usuario admin (del CSV).
    2. Procese y envíe los registros del archivo datos.csv.
    3. Cree una cita médica.
    4. Imprima en consola el JSON con la cita creada.
"""

import os
import requests
from requests.exceptions import RequestException
import pandas
from argparse import ArgumentParser
from dotenv import load_dotenv
import modelo
#from modelo import OdontocareData
#from modelo import OdontocareLoader

# Defino la funcion con el codigo para limpiar la pantalla , el tipico clear
def clear():
    os.system('clear')



# Funcion de inicio.
def main():
    # Gestion de  argumentos.
    parser = ArgumentParser(
        prog = 'carga_inicial',
        description= 'Programa cliente que hace la carga inicial'
    )
    # Usamos parserargument, dest es el nombre del atributo al que nos devolverá el valor. type es el tipo de dato que es.
    """
    parser.add_argument("-a", "--admin_file", dest="admin_file", help= "el fichero csv de admins a cargar", default='../data/admin.csv', type=str)
    parser.add_argument("-d", "--doctor_file", dest="doctor_file", help= "el fichero csv de doctores a cargar", default='../data/doctores.csv', type=str)
    parser.add_argument("-s", "--secretarios_file", dest="secretarios_file", help= "el fichero csv de secretarios a cargar", default='../data/secretarios.csv', type=str)
    parser.add_argument("-c", "--centros_file", dest="centros_file", help= "el fichero csv de centros a cargar", default='../data/centros.csv', type=str)
    parser.add_argument("-p", "--pacientes_file", dest="pacientes_file", help= "el fichero csv de pacientes a cargar", default='../data/pacientes.csv', type=str)
    #parser.add_argument("-t", "--citas_file", dest="citas_file", help= "el fichero csv de citas a cargar", default='../data/citas.csv', type=str)
    """

    parser.add_argument("-a", "--admin_file", dest="admin_file", help= "el fichero csv de admins a cargar", type=str, required= True)
    parser.add_argument("-d", "--doctor_file", dest="doctor_file", help= "el fichero csv de doctores a cargar", type=str, required= True)
    parser.add_argument("-s", "--secretarios_file", dest="secretarios_file", help= "el fichero csv de secretarios a cargar", type=str, required= True)
    parser.add_argument("-c", "--centros_file", dest="centros_file", help= "el fichero csv de centros a cargar", type=str, required= True)
    parser.add_argument("-p", "--pacientes_file", dest="pacientes_file", help= "el fichero csv de pacientes a cargar", type=str, required= True)

    args = parser.parse_args()
    # Importamos las variables de entorno que tenemos en el modelo, para ello usamos load_dotenv pero pasandole un stream del fichero que queremos.
    load_dotenv()

    #print(f"MAIN {args.filename}")
    data =  modelo.OdontocareData(
                            admin_file= args.admin_file,
                            centros_file= args.centros_file,
                            cita_file = ' ',
                            dr_file = args.doctor_file,
                            paciente_file= args.pacientes_file,
                            secretario_file= args.secretarios_file
                            )
    data.readData()

    loader = modelo.OdontocareLoader(data = data)
    loader.load()

    # Bloque para crear una cita.
    # Primero me logeo con un admin.
    token = None
    for admin in data.admins:
        response = requests.post(url = f'http://{os.getenv('AUTH_SERVER')}:{os.getenv('AUTH_PORT')}/auth/login', json = {'user' :  admin.username, 'password': admin.password})
        if response.status_code == 200:
            token = response.json().get('token')
    if token is None:
        print(f'ERROR al logear, no hemos podido hacer login.')
        exit (1)

    data_cita = {}
    data_cita['id_doctor'] = 1
    data_cita['id_centro'] = 1
    data_cita['id_paciente'] = 1
    data_cita['motivo'] = 'Dolor de encias'
    data_cita['fecha'] = '22/02/2026 18:30:00'

    
    response = requests.post(url = f'http://{os.getenv('CITAS_SERVER')}:{os.getenv('CITAS_PORT')}/citas/citas', json = data_cita, headers={'Authorization': f'Bearer {token}'})
    if response.status_code == 200:
        print (f'Cita creada con exito: request: {data_cita} \n\n response {response.json()}')
        exit (0)
    else:
        print (f'Error al crear la cita: request: {data_cita} \n\n response {response}; server http://{os.getenv('CITAS_SERVER')}:{os.getenv('CITAS_PORT')}/citas')
        exit (1)
    

if __name__ == '__main__':
    main()
