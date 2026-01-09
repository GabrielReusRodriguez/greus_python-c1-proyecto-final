import requests
import os
#from requests.exceptions import RequestException
from .odontocare_data import OdontocareData
from .admin import Admin
from .cita import Cita
from .centro import Centro
from .doctor import Doctor
from .paciente import Paciente
from .secretario import Secretario
from dotenv import load_dotenv

"""
En esta clase recibimos uns instancia de OdontocareData que básicamente tiene listas de instancias de Admin, Centro, Doctor, Cita...

Para que acabemso iterando una por una y enviándolas todas al WS correspondiente.

"""

class OdontocareLoader():

    USERNAME = ''
    PASSWORD = ''
    AUTH_URL = ''
    ADMIN_URL = ''
    CITAS_URL = ''

    #AUTH_URL = 'http://localhost:2203/auth'
    #ADMIN_URL = 'http://localhost:2204/admin'
    #CITAS_URL = 'http://localhost:2205/citas'

    def __init__(self, data: OdontocareData):
        
        global USERNAME
        global PASSWORD
        global AUTH_URL
        global ADMIN_URL
        global CITAS_URL

        self.data = data
        self.token = None
        self.id_usuario_logged = None
        # Creo unos diccionarios donde  guardaré los datos con la clave id_file para acceder más rapido ( no tener que iterar la lista cada vez )
        # cuando entremos las citas ( tienen id_doctor, id_centro...) 
        self.centros = {}
        self.admins = {}
        self.secretarios = {}
        self.pacientes= {}
        self.doctores = {}


        # Importo el fichero .env donde tengo usuario y contraseña de inicuio del admin.
        load_dotenv()
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')

        AUTH_URL =  f'http://{os.getenv('AUTH_SERVER')}:{os.getenv('AUTH_PORT')}/auth'
        ADMIN_URL = f'http://{os.getenv('ADMIN_SERVER')}:{os.getenv('ADMIN_PORT')}/admin'
        CITAS_URL = f'http://{os.getenv('CITAS_SERVER')}:{os.getenv('CITAS_PORT')}/citas'

    # Defino los webservices de la api rest 
    def _ws_login(self, user: str, password: str) -> requests.Response:
        global AUTH_URL
        data = {'user' : user, 'password' : password}
        response = requests.post(url = f'{AUTH_URL}/login', json = data)
        if response.status_code == 200:
            self.token = response.json()['token']
        else:
            print(f'Error al hacer login user {user}')
        return response
    
    def _ws_get_logged_user_id(self, token: str) -> requests.Response:
        global AUTH_URL
        response = requests.get(url = f'{AUTH_URL}/id', headers = {'Authorization' : f'Bearer {token}'})
        return response

    def _ws_new_user(self, token: str,user: dict) -> requests.Response:
        data = {    'username': user['username'], 
                    'password': user['password'], 
                    'rol':      user['rol']
        }
        global AUTH_URL
        response = requests.post(url = f'{AUTH_URL}/create_user', json = data, headers = {'Authorization' : f'Bearer {token}'})
        return response

    def _ws_new_admin(self, token: str, admin: dict) -> requests.Response:
        data = {    'username': admin['username'], 
                    'password': admin['password'], 
                    'rol':      'admin'
        }
        return self._ws_new_user(token = token, user = data)
    
    def _ws_new_secretario(self, token: str, secretario: dict) -> requests.Response:
        data = {    'username': secretario['username'], 
                    'password': secretario['password'], 
                    'rol':      'secretario'
        }
        return self._ws_new_user(token = token, user = data)

    
    def _ws_new_doctor(self,token: str, dr: dict) -> requests.Response:
        global ADMIN_URL
        data = {
                    'username':     dr['username'], 
                    'password':     dr['password'], 
                    'rol':          'doctor',
                    'nombre':       dr['nombre'],
                    'especialidad': dr['especialidad']
        }
        return requests.post(url = f'{ADMIN_URL}/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})


    def _ws_new_paciente(self, token: str, paciente: dict) -> requests.Response:
        global ADMIN_URL
        data = {
                    'username':     paciente['username'], 
                    'password':     paciente['password'], 
                    'rol':          'paciente',
                    'nombre':       paciente['nombre'],
                    'telefono':     paciente['telefono'],
                    'estado':       paciente['estado']
        }
        return requests.post(url = f'{ADMIN_URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    def _ws_new_centro(self, token: str, centro: dict) -> requests.Response:
        global ADMIN_URL
        data =  {
                    'direccion':    centro['direccion'],
                    'nombre':       centro['nombre']
        }
        return requests.post(url = f'{ADMIN_URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    def _ws_new_cita(self, token: str, cita: dict) -> requests.Response:
        global CITAS_URL
        """
                    id_cita (PK)
            fecha
            motivo
            estado
            id_paciente (FK)
            id_doctor (FK)
            id_centro (FK)
            id_usuario_registra(FK)
        """
        data =  {
                    'fecha':                cita['fecha'],
                    'motivo':               cita['motivo'],
                    'estado':               cita['estado'],
                    'id_paciente':          cita['id_paciente'],
                    'id_doctor':            cita['id_doctor'],
                    'id_centro':            cita['id_centro'],
                    'id_usuario_registra':  cita['id_usuario_registra']
        }
        return requests.post(url = f'{CITAS_URL}/citas', json = data, headers = {'Authorization' : f'Bearer {token}'})

    # Defino las funciones que implementan los pasos para enviar los nuevos datos para cada caso.
    def _new_admin(self, admin:Admin) -> requests.Response:
        response = self._ws_new_admin(token= self.token, admin = admin.to_dict())
        if response.status_code == 200:
            admin.from_dict(diccionario=response.json()['payload'])
            self.admins[admin.id_in_file] = admin.id_usuario
        return response

    def _new_secretario(self, secretario: Secretario) -> requests.Response:
        response = self._ws_new_secretario(token= self.token,secretario= secretario.to_dict())
        if response.status_code == 200:
            secretario.from_dict(diccionario= response.json()['payload'])
            self.secretarios[secretario.id_in_file] = secretario.id_usuario
        return response
    
    def _new_doctor(self, dr : Doctor) -> requests.Response:
        response = self._ws_new_doctor(token= self.token, dr= dr.to_dict())
        if response.status_code == 200:
            dr.from_dict(response.json()['payload'])
            self.doctores[dr.id_in_file] = dr.id_doctor
        return response

    def _new_centro(self, centro: Centro) -> requests.Response:
        response = self._ws_new_centro(token= self.token, centro = centro.to_dict())
        print(f'CENTRO: {response}')
        if response.status_code == 200:
            centro.from_dict(diccionario= response.json()['payload'])
            self.centros[centro.id_in_file] = centro.id_centro
        return response

    def _new_cita(self, cita: Cita) ->requests.Response:
        response = self._ws_new_cita(token= self.token, cita = cita.to_dict())
        if response.status_code == 200:
            cita.from_dict(diccionario= response.json()['payload'])
        return response
    
    def _new_paciente(self, paciente: Paciente) -> requests.Response:
        response = self._ws_new_paciente(token = self.token, paciente = paciente.to_dict())
        if response.status_code == 200:
            paciente.from_dict(diccionario=response.json()['payload'])
        return response

    # Funciones de carga
    def load(self):
        global USERNAME
        global PASSWORD
        response = self._ws_login(user= USERNAME, password= PASSWORD)
        if response.status_code != 200 or self.token is None:
            return
        # Con un if llenos de ands, consigo que al primero que falle, salga y no ejecute el resto.
        if (    self._load_admins() and 
                self._load_centros() and
                self._load_secretarios() and
                self._load_pacientes() and
                self._load_doctors() and
                self._load_citas()
        ):
            return

    def _load_admins(self):
        is_Error = False
        is_primer_admin = True
        for admin in self.data.admins:
            response = self._new_admin(admin = admin)
            if response.status_code != 200:
                is_Error = True
                print(f'ERROR: hemos detectado un error al crear un admin, return code -> {response.status_code} msg -> {response.json()['msg']}')
                break
                # Si es el primer admin agregado, hago login al nuevo para no hacer todo con el admin default.
            if is_primer_admin:
                response_login = self._ws_login(user = admin.username, password= admin.password)
                if response_login.status_code != 200:
                    print(f'ERROR: hemos detectado un error al hacer login, return code -> {response.status_code} msg -> {response.json()['msg']}')
                    is_Error = True
                    break
                # Obtengo el id de usuario logado.
                response_id = self._ws_get_logged_user_id(token = self.token)
                if response_id.status_code != 200:
                    isError = True
                    print(f'ERROR: hemos detectado un error al obtener la id del admin, return code -> {response.status_code} msg -> {response.json()['msg']}')
                    break
                if response_id.json().get('payload') is None or response_id.json().get('payload').get('id') is None:
                    isError = True
                    print(f'ERROR: hemos detectado un error al obtener la id del admin, return code -> {response.status_code} msg -> {response.json()['msg']}')
                    break
                self.id_usuario_logged = response_id.json()['payload']['id']
                is_primer_admin = False
        return is_Error
        
    def _load_doctors(self):
        is_Error = False
        for doctor in self.data.doctores:
            response = self._new_doctor(dr = doctor)
            if response.status_code != 200:
                is_Error = True
                print(f'ERROR: hemos detectado un error al crear un doctor, return code -> {response.status_code} msg -> {response.json()['msg']}')
                break
        return is_Error

    def _load_secretarios(self):
        is_Error = False
        for secretario in self.data.secretarios:
            response = self._new_secretario(secretario= secretario)
            if response.status_code != 200:
                is_Error = True
                print(f'ERROR: hemos detectado un error al crear un secretario, return code -> {response.status_code} msg -> {response.json()['msg']}')
                break
        return is_Error

    def _load_centros(self):
        is_Error = False
        for centro in self.data.centros:
            response = self._new_centro(centro = centro)
            # En caso que haya un error, paro y salgo.
            if response.status_code != 200:
                is_Error = True
                #print(f'ERROR: hemos detectado un error al crear un centro, return code -> {response.status_code} msg -> {response.json()['msg']}')
                print(f'ERROR: hemos detectado un error al crear un centro, return code -> {response}')
                break
        return is_Error

    def _load_pacientes(self):
        is_Error = False
        for paciente in self.data.pacientes:
            response = self._new_paciente(paciente= paciente)
            if response.status_code != 200:
                is_Error = True
                print(f'ERROR: hemos detectado un error al crear un paciente, return code -> {response.status_code} msg -> {response.json()['msg']}')
                break
        return is_Error
        
    # Carga las citas
    def _load_citas(self):
        is_Error = False
        for cita in self.data.citas:
            # Vamos a buscar los ids de las entidades creadas en el WS ya que tenemos las ids de los ficheros.
            id_centro = self.centros.get(cita.id_centro)
            id_dr = self.doctores.get(cita.id_doctor)
            id_paciente = self.pacientes.get(cita.id_paciente)
            if id_centro is None or id_dr is None or id_paciente is None:
                isError = True
                print(f'ERROR: hemos encontrado un campo que falta creando citas id_centro:{id_centro}, id_dr: {id_dr}, id_paciente: {id_paciente}')
                break
            cita.id_centro = id_centro
            cita.id_doctor = id_doctor
            cita.id_paciente = id_paciente
            cita.id_usuario_registra = self.id_usuario_logged
            response = self._ws_new_cita(cita= cita)
            if response.status_code != 200:
                isError = True
                print(f'ERROR: hemos detectado un error al crear la cita, return code -> {response.status_code} msg -> {response.json()['msg']}')
                break
        return isError
        

    