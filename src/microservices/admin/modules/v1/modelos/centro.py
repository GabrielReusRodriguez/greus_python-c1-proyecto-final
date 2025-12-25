"""
Este script modela la entidad centro. Es una clase que ejerce de ORM y abstrae la gestión de los datos con la BBDD.
Usaremos el modelo declarativo de SQLAlchemy para usar el ORM.
"""
from db import db

class CentroMedico(db.Model):
    """
        Centro medico
            id_centro (PK)
            nombre
            direccion
    """
    # Nombre de la tabla
    __tablename__ = 'centros'
    # Las columnas
    id_centro = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nombre = db.Column(db.String, nullable = False)
    direccion = db.Column(db.String, nullable = False)
    
    def to_dict(self):
        # Método para convertir el objeto en un diccionario.
        dictionary = {}
        dictionary['id_centro'] = self.id_centro
        dictionary['nombre'] = self.nombre
        dictionary['direccion'] = self.direccion
        return dictionary
    
