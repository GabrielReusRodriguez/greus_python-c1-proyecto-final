
from .usuario import Usuario

class Secretario(Usuario):

    def __init__(self, int, username: str, password :str):
        Usuario.__init__(self, username= username, password= password, rol = 'secretario')

    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        return diccionario
        
