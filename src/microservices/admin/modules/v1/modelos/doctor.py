"""
Este script modela la entidad doctor. Es una clase que ejerce de ORM y abstrae la gestión de los datos con la BBDD.
Usaremos el modelo declarativo de SQLAlchemy para usar el ORM.
"""
from db import db

class Doctor(db.Model):
    """
        Doctor
            id_doctor
            id_usuario (FK)
            nombre
            especialidad
    """
    # Nombre de la tabla
    __tablename__ = 'doctores'
    # Las columnas
    id_doctor = db.Column(db.Integer, autoincrement = True, primary_key = True)
    # No puedo declararla como FK de SQLAlchemy ya que la bbdd está en otro contenedor y NO se pueden ver. 
    # La integridad referencial se tendrá que hacer a mano.
    id_usuario = db.Column(db.Integer, nullable = False)
    nombre = db.Column(db.String, nullable = False)
    especialidad = db.Column(db.String, nullable = False)
    
    def to_dict(self):
        # Método para convertir el objeto en un diccionario.
        dictionary = {}
        dictionary['id_doctor'] = self.id_doctor
        dictionary['id_usuario'] = self.id_usuario
        dictionary['nombre'] = self.nombre
        dictionary['especialidad'] = self.especialidad
        return dictionary
    
