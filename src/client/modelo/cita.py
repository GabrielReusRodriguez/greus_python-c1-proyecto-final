
class Cita():

    def __init__(self, fecha: str, motivo: str, estado: str, id_paciente: int, id_doctor: int, id_centro: int , id_usuario: int):
        self.fecha = fecha
        self.motivo = motivo
        self.estado = estado
        self.id_centro = id_centro
        self.id_doctor = id_doctor
        self.id_paciente = id_paciente
        self.id_usuario = id_usuario

    def to_dict(self):
        diccionario = {}

        diccionario['fecha'] = self.fecha
        diccionario['motivo'] = self.motivo
        diccionario['estado'] = self.estado
        diccionario['id_centro'] = self.id_centro
        diccionario['id_doctor'] = self.id_doctor
        diccionario['id_paciente'] = self.id_paciente
        diccionario['id_usuario'] = self.id_usuario

        return diccionario