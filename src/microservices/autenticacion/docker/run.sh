#!/bin/env bash

# -d es para que se ejecute en background , dettached.
# --env-file .env es para especificarle el fichero de variables de environmnet a docker.
docker run  --env-file ./.env -d -p 2203:2203 uoc-autenticacion