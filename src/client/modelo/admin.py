
from .usuario import Usuario

class Admin(Usuario):

    def __init__(self, int, username: str, password :str):
        Usuario.__init__(self, username= username, password= password, rol = 'admin')

    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        return diccionario
        
