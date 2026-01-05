#!/bin/env python3

import os
# Para usar el input para el password y que printe * 
from getpass import getpass
import requests
from requests.exceptions import RequestException

# Defino la funcion con el codigo para limpiar la pantalla , el tipico clear
def clear():
    os.system('clear')


MAX_NUM_INTENTOS_LOGIN = 3


JWT_TOKEN = ''
USERNAME = ''
ROL = ''

def login():
    num_intentos_login = 0
    username = ''
    password = ''
    clear()
    while num_intentos_login < MAX_NUM_INTENTOS_LOGIN:
        # Mientras sea en blanco, volvemos a preguntar
        username= ''
        while (len(username) == 0):
            username = input("username: ")
            if len(username) == 0:
                input(f"\tPor favor, introduce tu usuario")
                clear()
        # Mientras sea en blanco, volvemos a preguntar
        password = ''
        while (len(password) == 0):
            password = getpass()
            if len(password) == 0:
                input(f"\tPor favor, introduce tu password")
                #clear()
        # Tenemos los dos datos por lo que intentamos logear.
        try:
            json = {}
            json['user'] = username
            json['password'] = password
            #response = requests.post(url = 'http://localhost:2023/auth/login', json= f"{'user' : '{username}', 'password' : '{password}'}")
            response = requests.post(url = 'http://localhost:2203/auth/login', json= json)
            data = response.json()
            # En caso que me den el OK , me quedo el jwt y borro password
            if response.status_code == 200:
                JWT_TOKEN = data['token']
                USERNAME = username
                print(f"LOGGED!!!")
                input()
                break
            else:
                print(f"\tError: {data['msg']}")
                input()
                clear()
        except RequestException as e:
            print(f"\n\tError en la petición HTTP: {e}")
            input()
        num_intentos_login = num_intentos_login + 1
    # Comprobamos si nos hemos logado.
    if num_intentos_login >= MAX_NUM_INTENTOS_LOGIN  or len(JWT_TOKEN) == 0:
        print(f"\n\tERROR: Al intentar logearse, máximo número de intentos alcanzado. Prueba más tarde")
        return

def check_user_rol(rol:string)-> bool:
    data = {}
    data['rol'] = rol
    response = requests.get(url = 'http://localhost:2203/auth/check', params = data)
    return response.status_code == 200


# Funcion de inicio.
def main():
    #Primero pedimos la autenticacion.
    login()
    # Comprobamos si nos hemos logado.
    if  len(JWT_TOKEN) == 0:
        #print(f"\n\tERROR: Al intentar logearse, máximo número de intentos alcanzado. Prueba más tarde")
        return
    # Comprobamos cada rol y ejecutamos la logica del que toque...
    if check_user_rol('paciente') == True:
        pass
    if check_user_rol('secretario') == True:
        pass
    if check_user_rol('medico') == True:
        pass
    if check_user_rol('admin') == True:
        pass

if __name__ == '__main__':
    main()
