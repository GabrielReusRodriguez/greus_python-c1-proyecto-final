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



class OdontocareLoader():

    #USERNAME = 'admin'
    #PASSWORD = 'password'

    #AUTH_URL = 'http://localhost:2203/auth'
    #ADMIN_URL = 'http://localhost:2204/admin'
    #CITAS_URL = 'http://localhost:2205/citas'

    def __init__(self, data: OdontocareData):
        self.data = data
        self.token = None
        # Importo el fichero .env donde tengo usuario y contraseña de inicuio del admin.
        load_dotenv()
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')

        AUTH_URL =  f'http://{os.getenv('AUTH_SERVER')}:{os.getenv('AUTH_PORT')}/auth'
        ADMIN_URL = f'http://{os.getenv('ADMIN_SERVER')}:{os.getenv('ADMIN_PORT')}/admin'
        CITAS_URL = f'http://{os.getenv('CITAS_SERVER')}:{os.getenv('CITAS_PORT')}/citas'

    # Defino los webservices de la api rest 
    def _ws_login(user: str, password: str) -> requests.Response:
        data = {'user' : user, 'password' : password}
        response = requests.post(url = f'{AUTH_URL}/login', json = data)
        if response.status_code == 200:
            self.token = response.json()['token']
        else:
            print(f'Error al hacer login user {user}')
        return response
    
    def _ws_new_user(self, token: str,user: dict) -> requests.Response:
        data = {    'username': user['username'], 
                    'password': user['password'], 
                    'rol':      user['rol']
        }
        response = requests.post(url = f'{AUTH_URL}/create_user', json = data, headers = {'Authentication' : f'Bearer {token}'})
        return response

    def _ws_new_admin(self, token: str, admin: dict) -> requests.Response:
        data = {    'username': admin['username'], 
                    'password': admin['password'], 
                    'rol':      'admin'
        }
        return self._ws_new_user(token = token, user = data)
    
    def _ws_new_secretario(self, secretario: dict) -> requests.Response:
        data = {    'username': secretario['username'], 
                    'password': secretario['password'], 
                    'rol':      'secretario'
        }
        return self._ws_new_user(token = token, user = data)

    
    def _ws_new_doctor(self, dr: dict) -> requests.Response:
        data = {
                    'username':     dr['username'], 
                    'password':     dr['password'], 
                    'rol':          'doctor',
                    'nombre':       dr['nombre'],
                    'especialidad': dr['especialidad']
        }
        return requests.post(url = f'{ADMIN_URL}/doctores', json = data, headers = {'Authorization' : f'Bearer {token}'})


    def _ws_new_paciente(self, paciente: dict) -> requests.Response:
        data = {
                    'username':     paciente['username'], 
                    'password':     paciente['password'], 
                    'rol':          'paciente',
                    'nombre':       paciente['nombre'],
                    'telefono':     paciente['telefono'],
                    'estado':       paciente['estado']
        }
        return requests.post(url = f'{ADMIN_URL}/pacientes', json = data, headers = {'Authorization' : f'Bearer {token}'})

    def _ws_new_centro(self, centro: dict) -> requests.Response:
        data =  {
                    'direccion':    centro['direccion'],
                    'nombre':       centro['nombre']
        }
        return requests.post(url = f'{ADMIN_URL}/centros', json = data, headers = {'Authorization' : f'Bearer {token}'})

    def _ws_new_cita(self, cita: dict) -> requests.Response:
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
        response = self._ws_new_admin(admin = admin.to_dict())
        if response.status_code == 200:
            admin.from_dict(diccionario=response.json()['payload'])
        return response

    def _new_secretario(self, secretario: Secretario) -> requests.Response:
        response = self._ws_new_secretario(secretario= secretario.to_dict())
        if response.status_code == 200:
            secretario.from_dict(diccionario= response.json()['payload'])
        return response
    
    def _new_doctor(self, dr : Doctor) -> requests.Response:
        response = self._ws_new_doctor(dr= dr.to_dict())
        if response.status_code == 200:
            dr.from_dict(response.json()['payload'])
        return response

    def _new_centro(self, centro: Centro) -> requests.Response:
        response = self._ws_new_centro(centro = centro.to_dict())
        if response.status_code == 200:
            centro.from_dict(diccionario= response.json()['payload'])
        return response

    def _new_cita(self, cita: Cita) ->requests.Response:
        response = self._ws_new_cita(cita = cita.to_dict())
        if response.status_code == 200:
            cita.from_dict(diccionario= response.json()['payload'])
        return response

    # Funciones de carga
    def load(self):
        response = self._ws_login(user = self.USERNAME, password= self.PASSWORD)
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
                break
                # Si es el primer admin agregado, hago login al nuevo para no hacer todo con el admin default.
                if is_primer_admin:
                    response_login = self._ws_login(user = admin.username, password= admin.password)
                    if response_login.status_code != 200:
                        is_Error = False
                        break
                    is_primer_admin = False

        return is_Error
        
    def _load_doctors(self):
        is_Error = False
        for doctor in self.data.doctores:
            response = self._new_doctor(dr = doctor)
            if response.status_code != 200:
                is_Error = True
                break
        return is_Error

    def _load_secretarios(self):
        is_Error = False
        for secretario in self.data.secretarios:
            response = self._new_secretario(secretario= secretario)
            if response.status_code != 200:
                is_Error = True
                break
        return is_Error

    def _load_centros(self):
        is_Error = False
        for centro in self.data.centros:
            response = self._new_centro(centro = centro)
            # En caso que haya un error, paro y salgo.
            if response.status_code != 200:
                is_Error = True
                break
        return is_Error

    def _load_pacientes(self):
        is_Error = False
        for paciente in self.data.pacientes:
            response = self._ws_new_paciente(paciente= paciente)
            if response.status_code != 200:
                isError = True
        return isError
        

    def _load_citas(self):
        is_Error = False
        return isError
        

    