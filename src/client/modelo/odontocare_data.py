import pandas
from .admin import Admin
from .secretario import Secretario
from .paciente import Paciente
from .doctor import Doctor
from .centro import Centro


class OdontocareData():

    """
    def __init__(self, 
                    admin_file :str, 
                    secretarios_file: str, 
                    doctores_file: str, 
                    pacientes_file : str, 
                    centros_file : str, 
                    citas_file: str):
    """
    def __init__(self, admin_file: str, secretario_file: str, dr_file: str, paciente_file: str, centros_file: str, cita_file: str ):

        self.file_admins = admin_file
        self.file_secretarios = secretario_file
        self.file_drs = dr_file
        self.file_pacientes = paciente_file
        self.file_centros = centros_file
        self.file_citas = cita_file
        
        # Usuarios
        self.admins = []
        self.secretarios = []
        self.doctores = []
        self.pacientes = []

        # Centros
        self.centros = []

        # Citas
        self.citas = []
    
    def readData(self):
        if ( self._readAdmins() == False or
                self._readCentros() == False or 
                self._readDoctores() == False or 
                self._readSecretarios() == False or 
                self._readPacientes() == False
                #self._readCitas() == False 
            ):
                return 

    def _readAdmins(self):
        try:
            df = pandas.read_csv(filepath_or_buffer = self.file_admins, sep = ',')
        except FileNotFoundError as e:
            print(f'El fichero {self.file_admins} no existe o no se pude leer')
            return
        if df is None: 
            print(f'ERROR al cargar el dataframe de admin: {self.file_admins}')
        #print(f'Admins cargados \n {df}')
        # Itero una a una para crear los objetos.
        for r in df.itertuples(index = False):
            admin = Admin(id_in_file= r.id, username= r.username, password= r.password)
            self.admins.append(admin)
        """
        print(f' tamano : {len(self.admins)}')
        for admin in self.admins:
            print(f' admin: {admin.to_dict()}')
        """

    def _readSecretarios(self):
        try:
            df = pandas.read_csv(filepath_or_buffer = self.file_secretarios, sep = ',')
        except FileNotFoundError as e:
            print(f'El fichero {self.file_secretarios} no existe o no se pude leer')
            return
        if df is None: 
            print(f'ERROR al cargar el dataframe de secretarios: {self.file_secretarios}')
        #print(f'Admins cargados \n {df}')
        # Itero una a una para crear los objetos.
        for r in df.itertuples(index = False):
            secretario = Secretario(id_in_file= r.id, username= r.username, password= r.password)
            self.secretarios.append(secretario)

    def _readDoctores(self):
        try:
            df = pandas.read_csv(filepath_or_buffer = self.file_drs, sep = ',')
        except FileNotFoundError as e:
            print(f'El fichero {self.file_doctores} no existe o no se pude leer')
            return
        if df is None: 
            print(f'ERROR al cargar el dataframe de doctores: {self.file_drs}')
        #print(f'Admins cargados \n {df}')
        # Itero una a una para crear los objetos.
        for r in df.itertuples(index = False):
            dr = Doctor(id_in_file=r.id, username=r.username, password=r.password, nombre=r.nombre, especialidad= r.especialidad)
            self.doctores.append(dr)

    def _readPacientes(self):
        try:
            df = pandas.read_csv(filepath_or_buffer = self.file_pacientes, sep = ',')
        except FileNotFoundError as e:
            print(f'El fichero {self.file_pacientes} no existe o no se pude leer')
            return
        if df is None: 
            print(f'ERROR al cargar el dataframe de pacientes: {self.file_pacientes}')
        #print(f'Admins cargados \n {df}')
        # Itero una a una para crear los objetos.
        for r in df.itertuples(index = False):
            paciente = Paciente(id_in_file=r.id, username=r.username, password=r.password, nombre = r.nombre, telefono=r.telefono, estado=r.estado)
            self.pacientes.append(paciente)

    def _readCentros(self):
        try:
            df = pandas.read_csv(filepath_or_buffer = self.file_centros, sep = ',')
        except FileNotFoundError as e:
            print(f'El fichero {self.file_centros} no existe o no se pude leer')
            return
        if df is None: 
            print(f'ERROR al cargar el dataframe de pacientes: {self.file_centros}')
        print(f'Centros cargados \n {df}')
        # Itero una a una para crear los objetos.
        for r in df.itertuples(index = False):
            centro = Centro(nombre= r.nombre, direccion= r.direccion, id_in_file= r.id)
            self.centros.append(centro)

    def _readCitas(self):
        pass




    
