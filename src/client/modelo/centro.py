
class Centro():

    def __init__(self, nombre: str, direccion: str ):
        self.id_centro = None
        self.nombre = nombre, 
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