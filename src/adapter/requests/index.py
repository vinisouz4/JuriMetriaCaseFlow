import requests
import json
import asyncio
import aiohttp

from src.adapter.logging.logging import LoggerHandler


class Requests():
    def __init__(self):
        self.logger = LoggerHandler("Requests")


    # Depois adicionar a etapa de requisição async com asyncio

    async def __getProcessStatus(self, session, processNumber, url: str, headers: dict = None, payload: dict = None):
        try:
            self.logger.INFO(f"Getting process status: {processNumber}")

            async with session.get(url, headers=headers, data=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                
                else:
                    self.logger.ERROR(f"Error getting data from url: {response.status}")

            self.logger.INFO(f"Data from process number: {processNumber} retrieved successfully")

            return response
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from url: {e}")

    
    async def get(self, url: str, processNumber: list, headers: dict = None, payload: dict = None):

        """
        Parameters:
        - url (str): Url da requisição;
        - processNumber (list): Lista de números de processo;
        - headers (dict): Headers da requisição;
        - payload (dict): Dicionario com os dados de filtros para a requisicao.

        Returns:
        - Irá me retornar uma lista de dicionários com os dados de cada processo.
        """

        try:
            self.logger.INFO(f"Getting data from url: {url}")

            async with aiohttp.ClientSession() as session:
                tasks = [self.__getProcessStatus(session, process, url, headers, payload) for process in processNumber]
                response = await asyncio.gather(*tasks)

                return response

            

            self.logger.INFO(f"Data from url: {url} retrieved successfully")

            return response
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from url: {e}")




