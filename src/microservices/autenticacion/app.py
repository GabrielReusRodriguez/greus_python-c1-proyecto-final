# Ponemos esto para evitar el error de dependencias circulares.
# from __future__ import annotations
import os
import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from modules.v1.recursos.auth_bp import auth_v1_bp
from db import db

#db = None
app = None

# Creo la app y registro los blueprints.
def create_app():

    # Le indico a la función que la variable db y app es global.
#    global db 
    global app
    
    # Creo la app
    app = Flask(__name__)    

    # Primero leo la configuración del fichero .cfg, para ello necesito saber la ruta del script python.
    path = os.path.dirname(os.path.realpath(__file__))
    cfg_path = f"config.cfg"
    # Mando al parser leer la configuracion
    config = configparser.ConfigParser()
    config.read([cfg_path])

    # Creo el acceso a la BBDD SQLite.
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALchemy']['url']

    # Registro los blueprints, podría hacerlo con cualquier version
    #app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/v1')
    app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/')

    db.init_app(app)
    #Inicializo el SQLAlchemy
#    db = SQLAlchemy(app)
    # Creo e Inicializo las tablas
    with app.app_context():
        db.create_all()
    
    return app