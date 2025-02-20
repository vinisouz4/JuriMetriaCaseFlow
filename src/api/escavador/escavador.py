import asyncio
import json
import escavador
from escavador.v2 import Processo


from src.adapter.core.config import Settings
from src.adapter.logging.logging import LoggerHandler
from src.adapter.requests.index import Requests
from src.use_case.tribunais.tribunais import getTribunalNumber
from src.utils.utils import Utils



class apiEscavador():
    def __init__(self):
        self.requests = Requests()
        self.logger = LoggerHandler("getDataJud")
        self.util = Utils()
        self.settings = Settings()

    def __getSession(self):
        self.logger.INFO("Getting session")
        return escavador.config(self.settings.ESCAVADOR_KEY)
    
    def getProcessos(self, numeroProcesso):
        try:
            self.logger.INFO(f"Getting processos {numeroProcesso}")
            
            session = self.__getSession()

            processos = Processo.por_numero(numero_cnj=numeroProcesso)

            self.logger.INFO(f"Processos {processos}")

            return processos
        except Exception as e:
            self.logger.ERROR(f"Error getting processos {e}")
            return None