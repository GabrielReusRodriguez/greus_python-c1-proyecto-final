from app import create_app
import os
import configparser

# Creamos la instancia de la aplicacion ( esto llamará a la función encargada de crear la app flask y agregar las rutas)
app = create_app()

if __name__ == '__main__':

    # Arrancamos el server.
    # Primero leo la configuración del fichero .cfg, para ello necesito saber la ruta del script python.
    path = os.path.dirname(os.path.realpath(__file__))
    cfg_path = f"config.cfg"
    # Mando al parser leer la configuracion
    config = configparser.ConfigParser()
    config.read([cfg_path])
    # Levanto el Flask con el microservicio.
    app.run(
        host= config['autenticacion']['HOST'], 
        port= config['autenticacion']['PORT'], 
        debug = config['autenticacion']['DEBUG'] == 'yes'
    )