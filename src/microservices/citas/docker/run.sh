#!/bin/env bash

# -d es para que se ejecute en background , dettached.
# --env-file .env es para especificarle el fichero de variables de environmnet a docker.
# --network es para indicarle a que red de docker pertenece
# --ip asigna la ip que queremos.

#docker run --rm --network odontocare-network --ip 172.16.0.2 -p 2204:2204  uoc-admin 
#docker run --rm --network host  -p 2204:2204  uoc-admin
docker run -d --rm --env-file ./.env-urls --env-file ./.env --network host  uoc-citas 