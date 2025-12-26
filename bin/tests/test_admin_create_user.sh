#!/bin/env bash

echo -e "\t\t Create user admin **********************"
curl -H "Authorization:Bearer $1" --json '{"username": "admin2" , "password" : "gregorio", "rol" : "admin"}' http://localhost:2204/admin/usuario
