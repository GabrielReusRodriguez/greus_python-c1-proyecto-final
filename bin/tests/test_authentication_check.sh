#!/bin/env bash

echo -e "\tTesteando el microsevicio de Autenticacion Check de token JWT"

echo -e "\t\t Check jwt  **********************"
curl --get -H "Authorization:Bearer $1" http://localhost:2203/auth/check?rol=usuario
curl --get -H "Authorization:Bearer $1" http://localhost:2203/auth/check?rol=admin
