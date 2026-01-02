#!/bin/env bash

# Con docker ps -q  obtenemos los ids de los dockers ejecutandose.
docker  kill $(docker ps -q)
