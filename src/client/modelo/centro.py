
class Centro():

    def __init__(self, nombre: str, direccion: str, id_in_file: int ):
        # id_in_file es el identificador que tiene en el ficheor
        # Lo usaremos para vincular con las citas id_doctor id_usuario_registra...
        self.id_in_file = id_in_file
        self.id_centro = None
        self.nombre = nombre 
        self.direccion = direccion

    def to_dict(self):
        diccionario = {}
        if self.id_centro is not None:
            diccionario['id_centro']    = self.id_centro
        diccionario['nombre']           = self.nombre
        diccionario['direccion']        = self.direccion
        return diccionario
    
    def from_dict(self, diccionario: dict):
        self.id_centro  = diccionario.get('id_centro')
        self.nombre     = diccionario.get('nombre')
        self.direccion  = diccionario.get('direccion')