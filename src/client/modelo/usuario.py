
class Usuario():

    def __init__(self, username: str, password :str, rol : str):
        self.id_usuario = -1
        self.username = username
        self.password = password
        self.rol = rol

    def to_dict(self):
        diccionario = {}

        diccionario['username'] = self.username
        diccionario['password'] = self.password
        diccionario['rol'] = self.rol

        return diccionario