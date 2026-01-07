
class Usuario():

    def __init__(self, username: str, password :str, rol : str):
        self.id_usuario = None
        self.username   = username
        self.password   = password
        self.rol        = rol

    def to_dict(self):
        diccionario = {}
        if self.id_usuario is not None:
            diccionario['id_usuario'] = self.id_usuario
        diccionario['username'] = self.username
        diccionario['password'] = self.password
        diccionario['rol']      = self.rol
        return diccionario


    def from_dict(self, diccionario: dict):
        self.id_usuario = diccionario.get('id_usuario')
        self.username   = diccionario.get('username')
        self.password   = diccionario.get('password')
        self.rol        = diccionario.get('rol')
        