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
    parser.add_argument("-f", "--file", dest="filename", help= "el fichero csv a cargar", default='./data.csv', type=str)
    args = parser.parse_args()
    print(f"MAIN {args.filename}")
    data =  modelo.OdontocareData()
    loader = modelo.OdontocareLoader(data = data)

    #data =  modelo.odontocare_data.OdontocareData()
    #loader = modelo.odontocare_loader.OdontocareLoader(data = data)
    



if __name__ == '__main__':
    main()
