
import json
from datetime import datetime


from src.adapter.core.config import Settings
from src.adapter.dataframe.interface import IDataFrameAdapter
from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils


class ReadDataJud():
    def __init__(self, dataframe: IDataFrameAdapter):
        self.logger = LoggerHandler("ReadDataJud")
        self.dataframe = dataframe
        self.settings = Settings()
        self.utils = Utils()

    def readDataJud(self):
        try:

            """
            Metodo para buscar apenas o ultimo movimento de cada processo
            """

            self.logger.INFO(f"Reading data from DataJud DataLake, Date: {self.utils.getToday()}")

            dictData = json.load(
                open(
                    f"{self.settings.DATALAKE_URL}data_{self.utils.getToday()}.json", "r"
                )
            )

            self.logger.INFO("Data read successfully")

            resultado = []

            for process in dictData:
                for source in process["hits"]["hits"]:
                    movimentos = source["_source"]["movimentos"]
                    ultimo_movimento = max(movimentos, key=lambda x: datetime.strptime(x["dataHora"], "%Y-%m-%dT%H:%M:%S.%fZ"))

                    results = {
                        "processo": source["_source"]["numeroProcesso"],
                        "dataAjuizamento": source["_source"]["dataAjuizamento"],
                        "dataUltimoMovimento": ultimo_movimento["dataHora"],
                        "movimento": ultimo_movimento["nome"]
                    }

                    resultado.append(results)


            self.logger.INFO("Transforming data to DataFrame")

            df = self.dataframe.to_DataFrame(resultado)

            df = self.dataframe.to_datetime(df, ["dataUltimoMovimento"])

            self.logger.INFO("Data transformed successfully")

            return df

        except Exception as e:
            self.logger.ERROR(f"Error in readDataJud: {e}")
            return None
        
    def statusGrouped(self, df):
        try:
            self.logger.INFO("Starting statusGrouped")

            dfGrouped = self.dataframe.groupby(df, ["movimento"], {"processo": "count"})

            self.logger.INFO("Status grouped successfully")

            return dfGrouped

        except Exception as e:
            self.logger.ERROR(f"Error in statusGrouped: {e}")
            return None

    def statusCount(self, df, status: str, dateColumn: str, qtdDays: int):
        try:

            """
            Método para contar a quantidade de processos por status dentro do range de datas
            Desde a distribuição até a data atual
            Parâmetros:
            df: DataFrame
            status: Qual status deseja contar
            dateColumn: Coluna de data do DataFrame, no caso ideal considerar a coluna de distribuição (por enquanto)
            qtdDays: Quantidade de dias que deseja verificar a contagem (Exemplo: 30 dias, 7 dias)
            """

            self.logger.INFO("Starting statusCount")

            data = self.dataframe.to_datetime(
                df, 
                [dateColumn]
            )

            today = self.utils.getToday()

            rangeDays = self.dataframe.getPastDate(qtdDays, today)

            # Aplicar o filtro de range de data e status
            data = df[
                (df[dateColumn] >= rangeDays) & 
                (df["movimento"] == status)
            ].shape[0]

            self.logger.INFO(f"Status {status} counted successfully")

            return data

        except Exception as e:
            self.logger.ERROR(f"Error in statusCount: {e}")
            return None

    def getAllMoviments(self):
        try:

            """
            Metodo para buscar todas as movimentacoes e datas de cada movimentacao.
            """

            self.logger.INFO(f"Reading data from DataJud DataLake, Date: {self.utils.getToday()}")

            dictData = json.load(
                open(
                    f"{self.settings.DATALAKE_URL}data_{self.utils.getToday()}.json", "r"
                )
            )

            self.logger.INFO("Data read successfully")

            processoFormatado =[]

            for process in dictData:
                for source in process["hits"]["hits"]:
                    sources = source["_source"]
                    processo = {
                        "numeroProcesso": sources.get("numeroProcesso", ""),
                        "dataAjuizamento": self.utils.formatar_data(sources.get("dataAjuizamento", "")),
                    }

                    movimentos_ordenados = sorted(
                        sources.get("movimentos", []), 
                        key=lambda x: x["dataHora"]
                    )

                    processo["movimentos"] = [mov["nome"] for mov in movimentos_ordenados]
                    processo["dataMovimentacao"] = [self.utils.formatar_data(mov["dataHora"]) for mov in movimentos_ordenados]

                    processoFormatado.append(processo)

            df = self.dataframe.to_DataFrame(processoFormatado)

            self.logger.INFO("Data transformed successfully")
            
            return df

        except Exception as e:
            self.logger.ERROR(f"Error in readDataJud: {e}")
            return None

    def meanDateProcess(self, df):
        try:

            """
            Metodo para calcular a média de dias entre a data de ajuizamento e a data do ultimo movimento
            """

            self.logger.INFO("Starting meanDateProcess")

            df["dataAjuizamento"] = self.dataframe.to_datetime(df, ["dataAjuizamento"])
            # df["dataMovimentacao"] = self.dataframe.to_datetime(df, ["dataMovimentacao"])

            # df["dias"] = (df["dataMovimentacao"] - df["dataAjuizamento"]).dt.days

            # media = df["dias"].mean()

            self.logger.INFO("Mean calculated successfully")

            return df

        except Exception as e:
            self.logger.ERROR(f"Error in meanDateProcess: {e}")
            return None