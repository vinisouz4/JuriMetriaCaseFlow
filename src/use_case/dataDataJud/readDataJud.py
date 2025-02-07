from src.adapter.requests.index import Requests


class ReadDataJud():
    def __init__(self):
        self.requests = Requests()

    async def getData(self, url: str, processNumber: list, headers: dict = None, numberEndPoint: int = 1):
        """
        Parameters:
        - url (str): Url da requisição;
        - processNumber (list): Lista de números de processo;
        - headers (dict): Headers da requisição;
        - payload (dict): Dicionario com os dados de filtros para a requisicao;
        - numberEndPoint (int): Número do endpoint da requisição.

        Returns:
        - Irá me retornar uma lista de dicionários com os dados de cada processo.
        """

        return await self.requests.get(url, processNumber, headers, numberEndPoint)