import asyncio
import json
import escavador
from escavador.v2 import Processo
import asyncio
from rapidfuzz import fuzz


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
        self.listProcess = []
        self.executedProcess = 0
        self.lock = asyncio.Lock()

    def __getSession(self):
        self.logger.INFO("Getting session")
        return escavador.config(self.settings.ESCAVADOR_KEY)
    
    def formatListProcess(self, df):
        try:
            self.logger.INFO(f"Formatting list of process, len df {len(df)}")

            listProcess = df["external_number"].unique().tolist()

            listProcess = [processo for processo in listProcess if self.util.validadorCNJ(processo)]

            self.logger.INFO(f"Formatted list of process, len listProcess {len(listProcess)}")

            return listProcess
        except Exception as e:
            self.logger.ERROR(f"Error formatting list of process {e}")
            return None
    
    def getDataPolos(self, retornoEnvolvidos, nome, polo):
        """
        retornoEnvolvidos é uma lista do metodo Fontes que me retorna a lista dos envolvidos
        nome é o nome que eu quero buscar os dados
        polo é se ele é ativo ou passivo
        """

        listDataPolo = []

        for envolvido in retornoEnvolvidos:
            if (fuzz.ratio(envolvido.nome, nome) > 70):
                dictEnvolvido = {
                    f"{polo}": True,
                    "nome": nome,
                    "cpf": envolvido.cpf,
                    "cnpj": envolvido.cnpj
                }

                listDataPolo.append(dictEnvolvido)

        return listDataPolo


    async def __getProcessos(self, numeroProcesso, totalProcess):
        """
        Parametros:
            numeroProcesso: str -> Numero do processo a ser consultado
            totalProcess: int -> Total de processos a serem consultados
        """
        try:
            self.logger.INFO(f"Getting total process {totalProcess}")

            session = self.__getSession()

            processList = []

            processo = await asyncio.to_thread(
                Processo.por_numero,
                numero_cnj=numeroProcesso
            )

            if processo:
                dictProcess = {
                    "numeroProcesso": processo.numero_cnj,
                    "anoInicio": processo.ano_inicio,
                    "quantidadeMovimentacao": processo.quantidade_movimentacoes,
                    "dataUltimaMovimentacao": processo.data_ultima_movimentacao,
                    "poloAtivo": processo.titulo_polo_ativo,
                    "dataPoloAtivo": self.getDataPolos(processo.fontes[0].envolvidos , processo.titulo_polo_ativo, "Ativo"),
                    "poloPassivo": processo.titulo_polo_passivo,
                    "dataPoloPassivo": self.getDataPolos(processo.fontes[0].envolvidos , processo.titulo_polo_passivo, "Passivo"),
                    "dataInicio": processo.data_inicio,
                    "tribunal": processo.fontes[0].sigla,
                    "tipo": processo.fontes[0].capa.area if processo.fontes[0].capa else None,
                }

                self.listProcess.append(dictProcess)

            else:
                self.logger.INFO(f"Processo {numeroProcesso} not found")
                dictProcess = {
                    "numeroProcesso": numeroProcesso,
                    "anoInicio": None,
                    "quantidadeMovimentacao": None,
                    "dataUltimaMovimentacao": None,
                    "poloAtivo": None,
                    "poloPassivo": None,
                    "dataInicio": None,
                    "tribunal": None,
                    "tipo": None,
                }

                self.listProcess.append(dictProcess)

            self.logger.INFO(f"Got process")

            self.logger.INFO(f"Sleeping 3 seconds")
            await asyncio.sleep(3)

            async with self.lock:
                self.executedProcess += 1
                self.logger.INFO(f"Executed process {self.executedProcess}/{totalProcess} - {numeroProcesso}")

            return processList
        except Exception as e:
            self.logger.ERROR(f"Error getting processos {e}")
            return None

    async def getMultipleProcess(self, numerosProcesso: list):
        """
        Parametros:
            numerosProcesso: list -> Lista de processos a serem consultados
        """
        try:

            totalProcess = len(numerosProcesso)

            tasks = [self.__getProcessos(numeroProcesso, totalProcess) for numeroProcesso in numerosProcesso]
            await asyncio.gather(*tasks)

            return self.listProcess
        except Exception as e:
            self.logger.ERROR(f"Error getting multiple processos {e}")
            return None
        
    def saveData(self, listProcess:list):
        try:
            self.logger.INFO("Starting saving data")
            
            with open(f"./src/data/lake/data_escavador_{self.util.getToday().month}_{self.util.getToday().year}.json", "w") as f:
                
                request = asyncio.run(
                    self.getMultipleProcess(listProcess)
                )
                
                json.dump(
                    request, 
                    f, 
                    indent=4, 
                    ensure_ascii=False
                )
            
            self.logger.INFO("Data saved successfully")
        except Exception as e:
            self.logger.ERROR(f"Error in saveData: {e}")
            return None
