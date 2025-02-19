import requests
import json
import asyncio
import aiohttp
import certifi
import ssl

from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils
from src.use_case.tribunais.tribunais import getTribunalNumber


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
                    return {"processo": processNumber, "data": data}
                
                else:
                    self.logger.ERROR(f"Error getting data from url: {response.status}")

            return response
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from url: {e}")

    
    async def get(self, url: str, processNumber, headers: dict):

        """
        Parameters:
        - url (str): Url da requisição;
        - processNumber (dataframe): dataframe com os dados de processos e endpoint;
        - headers (dict): Headers da requisição;
        - payload (dict): Dicionario com os dados de filtros para a requisicao.

        Returns:
        - Irá me retornar uma lista de dicionários com os dados de cada processo.
        """

        try:
            
            self.logger.INFO(f"Getting data from url: {url}")

            dfgrouped = processNumber.groupby("endpoint_tribunal")["external_number"].apply(list).reset_index()

            responses = []

            # Certificado SSL para requisições https
            sslContext = ssl.create_default_context(cafile=certifi.where())

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=sslContext)) as session:
                tasks = []

                for index, row in dfgrouped.iterrows():
                    self.logger.DEBUG(f"Endpoint: {row['endpoint_tribunal']}")
                    endpoint = row["endpoint_tribunal"]
                    numberProcess = row["external_number"]
                    
                    newUrl = url + f"api_publica_trt{endpoint}/_search"

                    self.logger.INFO(f"Data from url: {newUrl} retrieved successfully")

                    tasks.extend([self.__getProcessStatus(session, process, newUrl, headers) for process in numberProcess])

                results = await asyncio.gather(*tasks)

                return results
            
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from url: {e}")




