# Ponemos esto para evitar el error de dependencias circulares.
# from __future__ import annotations

import os
from flask import Flask

from modules.v1.recursos.auth_bp import auth_v1_bp
from modules.v1.modelos.usuario import Usuario

from db import db

app = None


# Creo la app y registro los blueprints.
def create_app():

    # Le indico a la función que la variable db y app es global.
    global app
    global db
    
    # Creo la app
    app = Flask(__name__)    

    # Creo el acceso a la BBDD SQLite.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URL')
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Registro los blueprints, podría hacerlo con cualquier version
    #app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/v1')
    #app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/')
    app.register_blueprint(auth_v1_bp, url_prefix= '/auth')
    
    #Inicializo el SQLAlchemy
    db.init_app(app)

    # Creo e Inicializo las tablas
    with app.app_context():
        db.create_all()
        # Cargo los datos del primer admin de las variables de entorno.
        APP_ROOT_USERNAME = os.getenv('APP_ROOT_USERNAME')
        APP_ROOT_PASSWORD = os.getenv('APP_ROOT_PASSWORD')

        # Agrego un usuario admin by default.
        user = Usuario(username = APP_ROOT_USERNAME, password = APP_ROOT_PASSWORD, rol = 'admin')
        db.session.add(user)
        db.session.commit()
    
    return app