"""
Este script modela la entidad usuario. Es una clase que ejerce de ORM y abstrae la gestión de los datos con la BBDD.
Usaremos el modelo declarativo de SQLAlchemy para usar el ORM.
"""
from db import db

class Usuario(db.Model):
    """
        Usuario
            id_usuario (PK)
            username
            password
            rol (admin, medico, secretaria/o, paciente)
    """
    # Nombre de la tabla
    __tablename__ = 'usuarios'
    # Las columnas
    id_usuario = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    rol  =  db.Column(db.String, nullable = False)

    def to_dict(self):
        # Método para convertir el objeto en un diccionario.
        dictionary = {}
        dictionary['id_usuario'] = self.id_usuario
        dictionary['username'] = self.username
        dictionary['password'] = self.password
        dictionary['rol'] = self.rol
        return dictionary
    
