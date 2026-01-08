
class Usuario():

    def __init__(self, username: str, password :str, rol : str, id_in_file: int):
        # id_in_file es el identificador que tiene en el ficheor
        # Lo usaremos para vincular con las citas id_doctor id_usuario_registra...
        self.id_in_file = id_in_file
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
        