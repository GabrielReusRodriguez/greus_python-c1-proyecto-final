import requests
#from requests.exceptions import RequestException
from .odontocare_data import OdontocareData

class OdontocareLoader():

    USERNAME = 'admin'
    PASSWORD = 'password'

    AUTH_URL = 'http://localhost:2203/auth'
    ADMIN_URL = 'http://localhost:2204/admin'
    CITAS_URL = 'http://localhost:2205/citas'

    def __init__(self, data: OdontocareData):
        self.data = data

    # Defino los webservices de la api rest 
    def _ws_login(user: str, password: str) -> requests.Response:
        data = {'user' : user, 'password' : password}
        response = requests.post(url = f'{AUTH_URL}/login', json = data)
        return response
    
    def _ws_new_user(self, user: dict) -> requests.Response:
        

    def _ws_new_doctor(self, dr: dict) -> requests.Response:
        pass

    def _ws_new_paciente(self, paciente: dict) -> requests.Response:
        pass

    def _ws_new_centro(self, centro: dict) -> requests.Response:
        pass

    def _ws_new_cita(self, cita: dict) -> requests.Response:
        pass

    # Defino las funciones que implementan los pasos para enviar los nuevos datos para cada caso.
    def _new_admin(self) -> requests.Response:
        pass

    def _new_secretario(self) -> requests.Response:
        pass
    
    def _new_doctor(self) -> requests.Response:
        pass

    def _new_centro(self) -> requests.Response:
        pass

    def _new_cita(self) ->requests.Response:
        pass

    # Funciones de carga
    def load(self):
        pass

    def _load_first_admin(self):
        pass

    def _load_admins(self):
        pass

    def _load_doctors(self):
        pass

    def _load_secretarios(self):
        pass

    def _load_centros(self):
        pass

    def _load_citas(self):
        pass

    