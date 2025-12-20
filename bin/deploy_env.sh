#!/bin/env bash

echo "Deploy del entorno Proyecto Final de la microcredencial C1 de Pyhton UOC de Greusr"

VENV_PATH='./.venv'

python3 -m venv ${VENV_PATH} && bash -c "${VENV_PATH}/bin/pip3 install -r ./requirements.txt"
