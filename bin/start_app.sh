#!/bin/env bash

# Obtengo la carpeta del script.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ACTUAL_PATH=`(pwd)`

echo "Iniciando microservicios..."

#Init...

echo "PATH: ${ACTUAL_PATH}"
DEPLOY_FOLDER="${SCRIPT_DIR}/../deploy/"

# Deploy de helloWorld
#******************************************************************************
#rm -rf "${DEPLOY_FOLDER}"
#mkdir "${DEPLOY_FOLDER}"

#echo -e "\t  HelloWorld..."
#MICROSERVICE_FOLDER="${SCRIPT_DIR}/../src/microservices/helloWorld"
#cd "${MICROSERVICE_FOLDER}"
#cp ${MICROSERVICE_FOLDER}/docker/* "${DEPLOY_FOLDER}"
#cp "${MICROSERVICE_FOLDER}/config.cfg" "${DEPLOY_FOLDER}"
#cp ${MICROSERVICE_FOLDER}/*.py "${DEPLOY_FOLDER}"

#cd "${DEPLOY_FOLDER}"
# Mando construir la imagen.
#./build.sh
# ejecuto el contenedor.
#./run.sh
#cd ${ACTUAL_PATH}

# Creamos la red de bridge
#docker network create --driver bridge --subnet=172.16.0.0/24 --ip-range=172.16.0.0/24 --gateway=172.16.0.254  odontocare-network


# Deploy de autenticacion
#******************************************************************************

rm -rf "${DEPLOY_FOLDER}"
mkdir "${DEPLOY_FOLDER}"

# Deploy del microservicio de autenticacion.
echo -e "\t  Autenticacion..."
# Me quedo con la carpeta base del microservicio y cambio a la carpeta del microservicio
MICROSERVICE_FOLDER="${SCRIPT_DIR}/../src/microservices/autenticacion"
cd "${MICROSERVICE_FOLDER}"
#cp classes.
# Copio los ficheros para crear y ejecutar el docker
cp ${MICROSERVICE_FOLDER}/docker/* "${DEPLOY_FOLDER}"
# Copio los .env file
# EL del microservicio
cp "${MICROSERVICE_FOLDER}/.env" "${DEPLOY_FOLDER}"
# Y el global
cp "${SCRIPT_DIR}/../src/.env" "${DEPLOY_FOLDER}/.env-urls"
# Copio los ficheros pyhton (run.py y app.py)
cp ${MICROSERVICE_FOLDER}/*.py "${DEPLOY_FOLDER}"
# Copio la carpeta con los blueprints y la lógica del microservicio.
cp -r ${MICROSERVICE_FOLDER}/modules "${DEPLOY_FOLDER}/modules"
# Copio la carpeta de clases auxiliares.
cp -r "${MICROSERVICE_FOLDER}/../../classes" "${DEPLOY_FOLDER}/classes"

# Voy a la carpeta de deploy.
cd "${DEPLOY_FOLDER}"
# Mando construir la imagen.
./build.sh
# ejecuto el contenedor.
./run.sh


# Deploy de microservicio de admin ****************************************************

rm -rf "${DEPLOY_FOLDER}"
mkdir "${DEPLOY_FOLDER}"

# Deploy del microservicio de autenticacion.
echo -e "\t  Admin..."
# Me quedo con la carpeta base del microservicio y cambio a la carpeta del microservicio
MICROSERVICE_FOLDER="${SCRIPT_DIR}/../src/microservices/admin"
cd "${MICROSERVICE_FOLDER}"
#cp classes.
# Copio los ficheros para crear y ejecutar el docker
cp ${MICROSERVICE_FOLDER}/docker/* "${DEPLOY_FOLDER}"
# Copio los .env file
# EL del microservicio
cp "${MICROSERVICE_FOLDER}/.env" "${DEPLOY_FOLDER}"
# Y el global
cp "${SCRIPT_DIR}/../src/.env" "${DEPLOY_FOLDER}/.env-urls"
# Copio los ficheros pyhton (run.py y app.py)
cp ${MICROSERVICE_FOLDER}/*.py "${DEPLOY_FOLDER}"
# Copio la carpeta con los blueprints y la lógica del microservicio.
cp -r ${MICROSERVICE_FOLDER}/modules "${DEPLOY_FOLDER}/modules"
# Copio la carpeta de clases auxiliares.
cp -r "${MICROSERVICE_FOLDER}/../../classes" "${DEPLOY_FOLDER}/classes"

# Voy a la carpeta de deploy.
cd "${DEPLOY_FOLDER}"
# Mando construir la imagen.
./build.sh
# ejecuto el contenedor.
./run.sh

#Vuelvo a la carpeta inicial
cd ${ACTUAL_PATH}