#!/bin/env bash

# Obtengo la carpeta del propio script.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
#echo "BAS source : ${BASH_SOURCE[0]} ___ ${SCRIPT_DIR}"
VENV_PATH="${SCRIPT_DIR}/../.venv"


#$("${VENV_PATH}/bin/python3 ${SCRIPT_DIR}/../src/client/odontocare_client.py")

echo "DIR: ${SCRIPT_DIR}"
ORDEN="${VENV_PATH}/bin/python3 ${SCRIPT_DIR}/../src/client/carga_inicial.py \
            --admin_file ${SCRIPT_DIR}/../data/admins.csv \
            --doctor_file ${SCRIPT_DIR}/../data/doctores.csv \
            --secretarios_file ${SCRIPT_DIR}/../data/secretarios.csv \
            --centros_file ${SCRIPT_DIR}/../data/centros.csv \
            --pacientes_file ${SCRIPT_DIR}/../data/pacientes.csv "

#echo "EXECUTABLE: ${VENV_PATH}/bin/python3 --help"
#$("${VENV_PATH}/bin/python3" --help) 
#$(${VENV_PATH}/bin/python3) --help

#command <<< ${VENV_PATH}/bin/python3

echo "${ORDEN}" | bash

echo "FIN"