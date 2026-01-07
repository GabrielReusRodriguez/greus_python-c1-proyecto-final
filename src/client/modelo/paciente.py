
from .usuario import Usuario

class Paciente(Usuario):

    def __init__(self, int, username: str, password :str, nombre: str, telefono: str, estado: str):
        Usuario.__init__(self, username= username, password= password, rol = 'paciente')
        self.id_paciente = None
        self.nombre = nombre
        self.telefono = telefono
        self.estado = estado

    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        if self.id_paciente is not None:
            diccionario['id_paciente'] = self.id_paciente
        diccionario['nombre'] = self.nombre
        diccionario['telefono'] = self.telefono
        diccionario['estado'] = self.estado
        return diccionario
        
    def from_dict(self, diccionario: dict):
        Usuario.from_dict(self, diccionario= diccionario)
        self.id_paciente    = diccionario.get('id_paciente')
        self.nombre         = diccionario.get('nombre')
        self.telefono       = diccionario.get('telefono')
        self.estado         = diccionario.get('estado')
        
