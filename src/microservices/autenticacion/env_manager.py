# Este script se encarga de cargar las variables de entorno en vars globales para  poder ser importadas en otros scripts

import os

# Cargo las variables de entorno.

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_SESSION_TIME = int(os.getenv('JWT_SESSION_TIME'))

APP_ROOT_USERNAME = os.getenv('APP_ROOT_USERNAME')
APP_ROOT_PASSWORD = os.getenv('APP_ROOT_PASSWORD')