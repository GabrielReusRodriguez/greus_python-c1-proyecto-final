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
    parser.add_argument("-a", "--admin_file", dest="admin_file", help= "el fichero csv de admins a cargar", default='../data/admin.csv', type=str)
    parser.add_argument("-d", "--doctor_file", dest="doctor_file", help= "el fichero csv de doctores a cargar", default='../data/doctores.csv', type=str)
    parser.add_argument("-s", "--secretarios_file", dest="secretarios_file", help= "el fichero csv de secretarios a cargar", default='../data/secretarios.csv', type=str)
    parser.add_argument("-c", "--centros_file", dest="centros_file", help= "el fichero csv de centros a cargar", default='../data/centros.csv', type=str)
    parser.add_argument("-p", "--pacientes_file", dest="pacientes_file", help= "el fichero csv de pacientes a cargar", default='../data/pacientes.csv', type=str)
    #parser.add_argument("-t", "--citas_file", dest="citas_file", help= "el fichero csv de citas a cargar", default='../data/citas.csv', type=str)

    args = parser.parse_args()
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

    #data =  modelo.odontocare_data.OdontocareData()
    #loader = modelo.odontocare_loader.OdontocareLoader(data = data)
    



if __name__ == '__main__':
    main()
