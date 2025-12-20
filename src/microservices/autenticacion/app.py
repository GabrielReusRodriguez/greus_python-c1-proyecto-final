from flask import Flask
from recursos.autenticacion import autenticacion_bp

# Creo la app y registro los blueprints.
def create_app():
    # Creo la app
    app = Flask(__name__)
    # Registro los blueprints
    app.register_blueprint(autenticacion_bp, url_prefix= '/autenticacion/v1')
    return app