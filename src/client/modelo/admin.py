
from .usuario import Usuario

class Admin(Usuario):

    def __init__(self, id_in_file: int, username: str, password :str):
        Usuario.__init__(self, username= username, password= password, rol = 'admin', id_in_file= id_in_file)
    """
    def to_dict(self):
        diccionario = Usuario.to_dict(self)
        return diccionario
    """