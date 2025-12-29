# Ponemos esto para evitar el error de dependencias circulares.
# from __future__ import annotations

import os
from flask import Flask

from modules.v1.recursos.citas_bp import citas_v1_bp

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
    print(f"sqlalchemy url: {os.getenv('SQLALCHEMY_URL')}")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Registro los blueprints, podría hacerlo con cualquier version
    #app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/v1')
    #app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/')
    app.register_blueprint(citas_v1_bp, url_prefix= '/citas')
    
    #Inicializo el SQLAlchemy
    db.init_app(app)

    # Creo e Inicializo las tablas
    with app.app_context():
        db.create_all()
    
    return app