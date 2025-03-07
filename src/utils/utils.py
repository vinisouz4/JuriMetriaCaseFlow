import json
from datetime import datetime
from validate_docbr import CPF, CNPJ
from src.adapter.logging.logging import LoggerHandler
import pandas as pd

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

    def getToday(self):
        """
        Retorna a data de hoje no formato 'YYYY-MM-DD'
        """
        try:
            self.logger.INFO("Getting today's date")
            self.logger.INFO("Today's date retrieved successfully")

            return datetime.today()
        
        except Exception as e:
            self.logger.ERROR(f"Error getting today's date: {e}")
            return None

    def getLatLong(self, uf):
        try:

            """
            Método para retornar a latitude e longitude de um estado brasileiro
            """
            
            self.logger.INFO(f"Getting latitude and longitude from UF: {uf}")

            uf_coordinates = {
                "AC": (-9.0238, -70.8111), "AL": (-9.5713, -36.7820), "AP": (0.9020, -52.0030),
                "AM": (-3.4168, -65.8561), "BA": (-12.5797, -41.7007), "CE": (-5.4984, -39.3206),
                "DF": (-15.7998, -47.8645), "ES": (-19.1834, -40.3089), "GO": (-15.8270, -49.8362),
                "MA": (-5.4200, -45.4326), "MT": (-12.6819, -56.9211), "MS": (-20.7722, -54.7852),
                "MG": (-18.5122, -44.5550), "PA": (-3.4168, -52.4500), "PB": (-7.2399, -36.7819),
                "PR": (-24.6170, -51.9022), "PE": (-8.8137, -36.9541), "PI": (-6.6876, -42.7374),
                "RJ": (-22.9068, -43.1729), "RN": (-5.7945, -36.3205), "RS": (-30.0346, -51.2177),
                "RO": (-10.9472, -62.8278), "RR": (2.7376, -61.3790), "SC": (-27.2423, -50.2189),
                "SP": (-23.5505, -46.6333), "SE": (-10.5741, -37.3857), "TO": (-10.1753, -48.2982),
            }

            lat, long = uf_coordinates.get(uf, (None, None))

            self.logger.INFO(f"Latitude and longitude retrieved successfully")

            return lat, long
        
        except Exception as e:
            self.logger.ERROR(f"Error getting latitude and longitude: {e}")
            return None, None

    def formatar_data(self,data_src):
        return data_src.replace("T", " ").replace("Z", "")
    
    def getNumberMonth(self, month):
        self.logger.INFO(f"Getting number of month: {month}")
        months = {
            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6,
            "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
        }
        self.logger.INFO(f"Number of month retrieved successfully")
        return months.get(month, None)
    
    def validateDoc(self, doc):
        try:
            self.logger.INFO(f"Validating document: {doc}")
            
            doc = str(doc).replace(".", "").replace("-", "").replace("/", "")
            
            if len(doc) == 11:
                cpf = CPF()
                self.logger.INFO(f"Document validated successfully CPF")
                self.logger.INFO(f"{cpf.validate(doc)}")
                return cpf.validate(doc)
            
            elif len(doc) == 14:
                cnpj = CNPJ()
                self.logger.INFO(f"Document validated successfully CNPJ")
                self.logger.INFO(f"{cnpj.validate(doc)}")
                return cnpj.validate(doc)

            else:
                self.logger.INFO("Document not validated")
                return False
            
        except Exception as e:
            self.logger.ERROR(f"Error validating document: {e}")
            return False


    def findClient(self, df, clientList):
        try:
            self.logger.INFO(f"Finding client")

            df[["cpfAtivo", "cpfPassivo", "cnpjAtivo", "cnpjPassivo"]] = df[["cpfAtivo", "cpfPassivo", "cnpjAtivo", "cnpjPassivo"]].astype(str).fillna("")

            mask = df.apply(lambda row: any(client in row.values for client in clientList), axis=1)

            self.logger.INFO("Client not found")
            return df[mask]
        
        except Exception as e:
            self.logger.ERROR(f"Error finding client: {e}")
            return None
        
    def converter_tempo(self, tempo):
        try:
            if pd.isna(tempo):
                return 0
            tempo = str(tempo).lower()
            if "year" in tempo:
                return int(tempo.split()[0]) * 365
            if "month" in tempo:
                return int(tempo.split()[0]) * 30
            if "week" in tempo:
                return int(tempo.split()[0]) * 7
            if "day" in tempo:
                return int(tempo.split()[0])
            if "hour" in tempo:
                return int(tempo.split()[0]) / 24
            else:
                return 0
            
        except Exception as e:
            self.logger.ERROR(f"Error converting time: {e}")
            return None

    def validadorCNJ(self, numero_processo):
        """
        Validador de número CNJ no qual o numero não deve ter letras e deve ter 20 caracteres
        """
        try:
            return isinstance(numero_processo, str) and len(numero_processo) == 20 and numero_processo.isnumeric()
        except Exception as e:
            self.logger.ERROR(f"Error validating CNJ: {e}")
            return False