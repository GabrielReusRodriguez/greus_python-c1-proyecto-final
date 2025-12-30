
from db import db

"""
Cita Médica
Relaciona paciente, doctor y centro:
    id_cita (PK)
    fecha
    motivo
    estado
    id_paciente (FK)
    id_doctor (FK)
    id_centro (FK)
    id_usuario_registra(FK)
"""

class Citas(db.Model):
    # Nombre de tabla
    __tablename__ = 'citas'
    # Las columnas
    id_cita = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fecha = db.Column(db.DateTime, nullable = False)
    motivo = db.Column(db.String, nullable  = False)
    estado = db.Column(db.String, nullable = False)
    id_paciente = db.Column(db.Integer, nullable = False)
    id_doctor = db.Column(db.Integer, nullable = False)
    id_usuario_registra = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        # Transforma el objeto a diccionario.
        diccionario = {}
        diccionario['id_cita'] = self.id_cita
        diccionario['fecha'] = self.fecha
        diccionario['motivo'] = self.motivo
        diccionario['estado'] = self.estado
        diccionario['id_paciente'] = self.id_paciente
        diccionario['id_doctor'] = self.id_doctor
        diccionario['id_usuario_registra'] = self.id_usuario_registra
        return diccionario
