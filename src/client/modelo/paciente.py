
from .usuario import Usuario

class Paciente(Usuario):

    def __init__(self, int, username: str, password :str, nombre: str, telefono: str, estado: str):
        Usuario.__init__(self, username= username, password= password, rol = 'paciente')
        self.nombre = nombre
        self.telefono = telefono
        self.estado = estado

    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        
        diccionario['nombre'] = self.nombre
        diccionario['telefono'] = self.telefono
        diccionario['estado'] = self.estado

        return diccionario
        
