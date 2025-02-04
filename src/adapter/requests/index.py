import requests
import json
import asyncio
import aiohttp
import certifi
import ssl

from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils


class Requests():
    def __init__(self):
        self.logger = LoggerHandler("Requests")
        self.utils = Utils()

    async def __getProcessStatus(self, session, processNumber, url: str, headers: dict = None):

        """
        Metodo privado para fazer a requisição de status de um processo específico de forma assíncrona.
        """

        try:
            self.logger.INFO(f"Getting process status: {processNumber}")

            payload = self.utils.generatePayload(
                processNumber=processNumber,
                size=1,
                sortField="dataAjuizamento",
                sortOrder="desc"
            )

            async with session.get(url, headers=headers, data=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                
                else:
                    self.logger.ERROR(f"Error getting data from url: {response.status}")

            return response
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from url: {e}")

    
    async def get(self, url: str, processNumber: list, headers: dict, numberEndPoint: int):

        """
        Parameters:
        - url (str): Url da requisição;
        - processNumber (list): Lista de números de processo;
        - headers (dict): Headers da requisição;
        - payload (dict): Dicionario com os dados de filtros para a requisicao.
        - numberEndPoint (int): Número do endpoint da requisição.

        Returns:
        - Irá me retornar uma lista de dicionários com os dados de cada processo.
        """

        try:
            
            newUrl = url + f"api_publica_trt{numberEndPoint}/_search"
            
            self.logger.INFO(f"Getting data from url: {newUrl}")

            # Certificado SSL para requisições https
            sslContext = ssl.create_default_context(cafile=certifi.where())

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=sslContext)) as session:
                tasks = [self.__getProcessStatus(session, process, newUrl, headers) for process in processNumber]
                
                response = await asyncio.gather(*tasks)

                self.logger.INFO(f"Data from url: {newUrl} retrieved successfully")

                return response
            
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from url: {e}")




