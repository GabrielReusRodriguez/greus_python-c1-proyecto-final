#!/bin/env bash

# Con docker ps -q  obtenemos los ids de los dockers ejecutandose.
docker restart $(docker ps -q)
