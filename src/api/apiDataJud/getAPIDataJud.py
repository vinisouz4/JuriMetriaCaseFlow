from src.adapter.core.config import Settings
from src.adapter.logging.logging import LoggerHandler
from src.adapter.requests.index import Requests
import asyncio
import json

from src.use_case.tribunais.tribunais import getTribunalNumber
from src.utils.utils import Utils



class getDataJud():
    def __init__(self):
        self.requests = Requests()
        self.logger = LoggerHandler("getDataJud")
        self.util = Utils()
        self.settings = Settings()

    async def getData(self, url: str, processNumber, headers: dict = None):
        """
        Parameters:
        - url (str): Url da requisição;
        - processNumber (dataframe): Dataframe com os dados para a requisição contendo o numero do processo e o endpoint;
        - headers (dict): Headers da requisição;
        - payload (dict): Dicionario com os dados de filtros para a requisicao;
        - numberEndPoint (int): Número do endpoint da requisição.

        Returns:
        - Irá me retornar uma lista de dicionários com os dados de cada processo.
        """

        return await self.requests.get(url, processNumber, headers)
    
    
    def saveData(self, df):

        """
        Metodo para buscar os processo na API do DataJud e salvar um arquivo no Data Lake com os dados
        df -> Dataframe com os processos retornados no Escavador
        """

        try:
            self.logger.INFO("Starting saving data")

            # Após validacao, salvar os dados dentro de um data lake na nuvem ou fisico
            with open(f"./src/data/lake/data_{self.util.getToday().month}_{self.util.getToday().year}.json", "w") as f:

                request = asyncio.run(self.getData(
                    url = self.settings.API_PUBLI_DATAJUD, 
                    processNumber=df, 
                    headers={
                        "Authorization": self.settings.API_PUBLI_DATAJUD_KEY,
                        "Content-Type": "application/json"
                    }
                ))
                    
                json.dump(request, f, indent=4, ensure_ascii=False)
            
            self.logger.INFO("Data saved successfully")
        except Exception as e:
            self.logger.ERROR(f"Error in saveData: {e}")
            return None