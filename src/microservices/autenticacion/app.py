from flask import Flask
from modules.v1.recursos.auth_bp import auth_v1_bp

# Creo la app y registro los blueprints.
def create_app():
    # Creo la app
    app = Flask(__name__)
    # Registro los blueprints, podría hacerlo con cualquier version
    #app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/v1')
    app.register_blueprint(auth_v1_bp, url_prefix= '/autenticacion/')
    return app