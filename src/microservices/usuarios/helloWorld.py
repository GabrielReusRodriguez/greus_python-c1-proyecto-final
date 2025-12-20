"""
    Es un microservicio para comprobar que está arrancado.
"""
from flask import Flask, jsonify
import os
import configparser

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return jsonify({'mensaje' : 'OK'})

if __name__ == '__main__':
    # Obtengo la carpeta del fichero de configuracion
    path = os.path.dirname(os.path.realpath(__file__))
    #cfg_path = f"{path}/../../configs/microservices.cfg"
    # He creado un enlace simbólico al cfg centralizado para que pueda leerlo desde la carpeta del microservicio.
    #cfg_path = f"{path}/config.cfg"
    cfg_path = f"config.cfg"
    config = configparser.ConfigParser()
    config.read([cfg_path])
    # Levanto el Flask con el microservicio.
    app.run(
        host= config['helloWorld']['HOST'], 
        port= config['helloWorld']['PORT'], 
        debug = config['helloWorld']['DEBUG'] == 'yes'
        )
    
    