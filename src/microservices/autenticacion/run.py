from app import create_app
import os
import configparser

# Creamos la instancia de la aplicacion
app = create_app()

if __name__ == '__main__':

    # Arrancamos el server.
    path = os.path.dirname(os.path.realpath(__file__))
    cfg_path = f"{path}/config.cfg"
    config = configparser.ConfigParser()
    l= config.read([cfg_path])
    with open(cfg_path, 'r') as f:
        st = f.read()
    print(f"gabriel: {st}")
    # Levanto el Flask con el microservicio.
    
    app.run(
        host= config['autenticacion']['HOST'], 
        port= config['autenticacion']['PORT'], 
        debug = config['autenticacion']['DEBUG'] == 'yes'
    )
    
    """
    app.run(
        host= '0.0.0.0', 
        port= 2202, 
        debug = True
    )
    """
