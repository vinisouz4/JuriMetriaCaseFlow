
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
                        "data": ultimo_movimento["dataHora"],
                        "movimento": ultimo_movimento["nome"]
                    }

                    resultado.append(results)


            self.logger.INFO("Transforming data to DataFrame")

            df = self.dataframe.to_DataFrame(resultado)

            df = self.dataframe.to_datetime(df, ["data"])

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