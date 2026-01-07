
class Cita():

    def __init__(self, fecha: str, motivo: str, estado: str, id_paciente: int, id_doctor: int, id_centro: int , id_usuario: int):
        self.id_cita                = None
        self.fecha                  = fecha
        self.motivo                 = motivo
        self.estado                 = estado
        self.id_centro              = id_centro
        self.id_doctor              = id_doctor
        self.id_paciente            = id_paciente
        self.id_usuario_registra    = id_usuario

    def to_dict(self):
        diccionario = {}
        if self.id_cita is not None:
            diccionario['id_cita']          = self.id_cita
        diccionario['fecha']                = self.fecha
        diccionario['motivo']               = self.motivo
        diccionario['estado']               = self.estado
        diccionario['id_centro']            = self.id_centro
        diccionario['id_doctor']            = self.id_doctor
        diccionario['id_paciente']          = self.id_paciente
        diccionario['id_usuario_registra']  = self.id_usuario_registra

        return diccionario
    
    def from_dict(self, diccionario: dict):
        self.id_cita                = diccionario.get('id_cita')
        self.fecha                  = diccionario.get('fecha')
        self.motivo                 = diccionario.get('motivo')
        self.estado                 = diccionario.get('estado')
        self.id_centro              = diccionario.get('id_centro')
        self.id_doctor              = diccionario.get('id_doctor')
        self.id_paciente            = diccionario.get('id_paciente')
        self.id_usuario_registra    = diccionario.get('id_usuario_registra')