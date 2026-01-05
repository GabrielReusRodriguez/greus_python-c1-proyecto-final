
from .usuario import Usuario

class Doctor(Usuario):

    def __init__(self, int, username: str, password :str, nombre: str, especialidad: str):
        Usuario.__init__(self, username= username, password= password, rol = 'doctor')
        self.nombre = nombre
        self.especialidad = especialidad

    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        
        diccionario['nombre'] = self.nombre
        diccionario['especialidad'] = self.especialidad

        return diccionario
        
