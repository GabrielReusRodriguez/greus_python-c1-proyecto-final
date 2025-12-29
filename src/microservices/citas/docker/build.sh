#!/bin/env bash

# Obtengo las variables del fichero de variables de entorno .env-urls y se las paso como variable de tiempo de construccion a docker build
docker build $(for i in `cat .env-urls`; do out+="--build-arg $i " ; done; echo $out;out="") -t uoc-citas .
