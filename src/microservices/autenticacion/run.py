from app import create_app
import os

# Creamos la instancia de la aplicacion ( esto llamará a la función encargada de crear la app flask y agregar las rutas)
app = create_app()


if __name__ == '__main__':

    # Levanto el Flask con el microservicio.
    app.run(
        host= os.getenv('AUTHENTICATION_HOST'), 
        port= int(os.getenv('AUTHENTICATION_PORT')), 
        debug = os.getenv('AUTHENTICATION_DEBUG') == 'yes'
    )

