#!/bin/env bash

echo -e "\tTesteando el microsevicio de create user Autenticacion"

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "admin2" , "password" : "pwdasdasd", "rol" : "admin"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"user": "admin2" , "password" : "pwdasdasd", "rol" : "medico"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "admin2" , "passw" : "pwdasdasd", "rol" : "medico"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "admin2" , "password" : "pwdasdasd", "ro" : "medico"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "admin" , "password" : "pwdasdasd", "rol" : "medico"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "ggg1234" , "password" : "pwd", "rol" : "medico"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "ggg" , "password" : "pwd123456", "rol" : "medico"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user incorrecto **********************"
curl --json '{"username": "gggdasdqw" , "password" : "pwd123456", "rol" : "root"}' http://localhost:2203/auth/create_user

echo -e "\t\t Create user Correcto **********************"
curl --json '{"username": "gabriel4" , "password" : "pwd12345", "rol" : "medico"}' http://localhost:2203/auth/create_user
