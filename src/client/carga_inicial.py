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

from argparse import ArgumentParser
import requests
from requests import RequestException

JWT_TOKEN = ''


def _login()->bool :

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


def _carga_csv()->bool:
    pass

def _envia_csv()->bool:
    pass




def main():
    parser = ArgumentParser(
        prog = 'carga_inicial',
        description= 'Programa cliente que hace la carga inicial'
    )
    # Usamos parserargument, dest es el nombre del atributo al que nos devolverá el valor. type es el tipo de dato que es.
    parser.add_argument("-f", "--file", dest="filename", help= "el fichero csv a cargar", default='./data.csv', type=str)
    args = parser.parse_args()
    print(f"MAIN {args.filename}")


if __name__ == '__main__':
    main()
