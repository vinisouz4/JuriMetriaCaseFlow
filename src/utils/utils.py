import json

from src.adapter.logging.logging import LoggerHandler


class Utils():
    def __init__(self):
        self.logger = LoggerHandler("Utils")

    def generatePayload(self, processNumber: str, size: int, sortField: str, sortOrder: str, additionalFiltters: list = None):
        """
        Parameters:
        - processNumber (str): Número do processo que deseja buscar;
        - size (int): Tamanho da página e quantidade de registros que deseja buscar;
        - sortField (str): Nome do campo de data que deseja ordenar os registros;
        - additionalFiltters (list): Lista de filtros adicionais que deseja aplicar na busca:
            - Exemplo: [{"match": {"numeroProcesso": "10013836720245020262"}}]
        
        Returns:
        - Retorna o payload em forma de dicionario com os dados para realização dos filtros na requisição de busca.
        """
        try:
            self.logger.INFO(f"Generating payload for process: {processNumber}")

            mustCondition = [
                {
                    "match": {"numeroProcesso": f"{processNumber}"}
                }
            ]

            
            # Adiciona os demais filtros caso existam
            if additionalFiltters:
                mustCondition.extend(additionalFiltters)

            payload = json.dumps({
                "size": size,
                "query":
                {
                    "bool":
                    {
                        "must": mustCondition
                    }
                },
                "sort": 
                [
                    {
                        f"{sortField}":
                        {
                            "order": f"{sortOrder}"
                        }
                    }
                ]
            })

            self.logger.INFO(f"Payload generated successfully")

            return payload
        
        except Exception as e:
            self.logger.ERROR(f"Error generating payload: {e}")