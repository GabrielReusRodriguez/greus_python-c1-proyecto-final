"""
Este script modela la entidad paciente. Es una clase que ejerce de ORM y abstrae la gestión de los datos con la BBDD.
Usaremos el modelo declarativo de SQLAlchemy para usar el ORM.
"""
from db import db

class Paciente(db.Model):
    """
        Paciente
            id_paciente (PK)
            id_usuario (FK opcional)
            nombre
            teléfono
            estado(ACTIVO/INACTIVO)
    """
    # Nombre de la tabla
    __tablename__ = 'pacientes'
    # Las columnas
    id_paciente = db.Column(db.Integer, autoincrement = True, primary_key = True)
    # No puedo declararla como foreign key segun sqlalchemy ya que NO ve la tabla de usuarios que está en el docker de authenticacion.
    # La integridad referencial se manejará a mano en el codigo.
    id_usuario = db.Column(db.Integer, nullable = False)
    nombre =    db.Column(db.String, nullable = False)
    telefono = db.Column(db.String, nullable = False)
    estado  =  db.Column(db.String, nullable = False)

    def to_dict(self):
        # Método para convertir el objeto en un diccionario.
        dictionary = {}
        dictionary['id_paciente'] = self.id_paciente
        dictionary['id_usuario'] = self.id_usuario
        dictionary['nombre'] = self.nombre
        dictionary['telefono'] = self.telefono
        dictionary['estado'] = self.estado
        return dictionary
    
