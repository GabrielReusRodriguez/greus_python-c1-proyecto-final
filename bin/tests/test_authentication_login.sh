#!/bin/env bash

curl --request POST --json '{"user": "admin" , "password" : "password"}' http://localhost:2203/auth/login