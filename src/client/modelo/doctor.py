
from .usuario import Usuario

class Doctor(Usuario):

    def __init__(self, int, username: str, password :str, nombre: str, especialidad: str):
        Usuario.__init__(self, username= username, password= password, rol = 'doctor')
        self.id_doctor      = None
        self.nombre         = nombre
        self.especialidad   = especialidad

    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        if self.id_doctor is not None:
            diccionario['id_doctor'] = self.id_doctor
        diccionario['nombre']       = self.nombre
        diccionario['especialidad'] = self.especialidad
        return diccionario
    
    def from_dict(self, diccionario: dict):
        Usuario.from_dict(self, diccionario=diccionario)
        self.id_doctor      = diccionario.get('id_doctor')
        self.nombre         = diccionario.get('nombre')
        self.especialidad   = diccionario.get('especialidad')
