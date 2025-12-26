#!/bin/env bash

echo -e "\tTesteando el microsevicio de login Autenticacion"

echo -e "\t\t Login user incorrecto **********************"
curl --json '{"user": "gabriel2" , "password" : "pwd"}' http://localhost:2203/auth/login
echo -e "\t\t Login pwd incorrecto **********************"
curl --json '{"user": "gabriel" , "password" : "123"}' http://localhost:2203/auth/login
echo -e "\t\t Login Correcto **********************"
#curl --json '{"user": "admin" , "password" : "gregorio"}' http://172.16.0.1:2203/auth/login
curl --json '{"user": "admin" , "password" : "gregorio"}' http://localhost:2203/auth/login
