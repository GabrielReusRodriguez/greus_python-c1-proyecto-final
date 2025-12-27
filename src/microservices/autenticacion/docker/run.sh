#!/bin/env bash

# -d es para que se ejecute en background , dettached.
# --env-file .env es para especificarle el fichero de variables de environmnet a docker.
# --ip asigna la ip que queremos al contenedor.

#docker run  --rm --env-file ./.env -d --network odontocare-network --ip 172.16.0.1 -p 2203:2203  uoc-autenticacion
#docker run  --rm --env-file ./.env --env-file ./.env-urls -d --network host  uoc-autenticacion 
docker run  --rm --env-file ./.env --env-file ./.env-urls -d --network host  uoc-autenticacion 